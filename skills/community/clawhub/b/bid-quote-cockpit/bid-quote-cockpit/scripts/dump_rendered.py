#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dump_rendered.py — 渲染级文本导出/断言（看板交付前第 4 道检查）

为什么需要它：
  `grep` 只能扫源码。看板里大量数字是**客户端 JS 用 `fmt()` 现拼**的
  （千分位、正负号、单位后缀都不在源码里），所以「单位 ↔ 金额 是否配对」
  这类文案错配，静态扫描、JS 冒烟、版式溢出体检**三关都拦不住**。
  唯一可靠办法：真实浏览器渲染后取 `innerText` 再断言。

用法：
  # 1) 只看渲染文本（排错用）
  python dump_rendered.py 看板.html --ids tScoreNoFac,scoreNoFacNote

  # 2) 跑断言文件（交付闸门用，exit 非 0 = 不可交付）
  python dump_rendered.py 看板.html --ids tScore,scoreNote --rules rules.json

rules.json 格式（全部可选，按需组合）：
{
  "_note":           "★ 以 `_` 开头的键是注释，会被自动忽略，不会当成容器 id。",
  "scoreNote": {
    "must_contain":    ["甲公司", "123,456.00"],
    "must_not_match":  ["最低为\\s*乙公司\\s*€?\\s*123,456"],
    "must_match":      ["最低为\\s*甲公司"]
  },
  "tScore": { "must_not_contain": ["NaN", "undefined"] }
}

四类断言：`must_contain` / `must_not_contain`（子串）、`must_match` / `must_not_match`（正则）。

约定：
  · **`_` 前缀键 = 注释**，不参与渲染与断言；
  · 规则里出现的 id 会自动并入渲染清单（不必再写进 `--ids`）；
  · 容器不存在 → 返回哨兵 `__MISSING__`（断言里可直接判它）；
  · `<table>` 容器自动按「每行 = ` | ` 拼接单元格」导出，便于逐行断言；
  · 其他容器导出 `innerText` 压平空白后的单行。

依赖：本机 Chrome（与 check_overflow.py 同一套候选路径），无需 pip 安装。
"""

import argparse
import html as _html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

PROBE_TPL = """
<script>
(function(){
  var IDS = __IDS__;
  function flat(el){ return (el.innerText || el.textContent || '').replace(/\\s+/g,' ').trim(); }
  function rows(tb){
    return Array.prototype.map.call(tb.querySelectorAll('tr'), function(tr){
      return Array.prototype.map.call(tr.querySelectorAll('th,td'), function(c){
        return (c.innerText||c.textContent||'').replace(/\\s+/g,' ').trim();
      }).join(' | ');
    }).join('\\n');
  }
  var out = {};
  IDS.forEach(function(id){
    var el = document.getElementById(id);
    if(!el){ out[id] = '__MISSING__'; return; }
    out[id] = (el.tagName === 'TABLE') ? rows(el)
            : (el.querySelector && el.querySelector('table') ? rows(el.querySelector('table'))
               : flat(el));
  });
  var pre = document.createElement('pre');
  pre.id = '__rendered';
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
})();
</script>
"""


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def render_texts(html_path, ids, width=1500, budget=9000):
    chrome = find_chrome()
    if not chrome:
        raise RuntimeError("未找到 Chrome，无法做渲染级检查（候选：%s）" % CHROME_CANDIDATES)

    src = io.open(html_path, "rb").read().decode("utf-8")
    i = src.rfind("</body>")              # ⚠️ 必须 rfind：echarts 压缩码里有字面量 '</body>'
    if i < 0:
        i = src.rfind("</html>")
    if i < 0:
        raise RuntimeError("HTML 里找不到 </body> / </html>，无法注入探针")

    probe = PROBE_TPL.replace("__IDS__", json.dumps(ids, ensure_ascii=False))
    out_html = src[:i] + probe + src[i:]

    tmpdir = tempfile.mkdtemp(prefix="dumprend_")
    try:
        p_html = os.path.join(tmpdir, "probe.html")
        io.open(p_html, "w", encoding="utf-8", newline="").write(out_html)
        url = "file:///" + p_html.replace("\\", "/")
        p = subprocess.run(
            [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
             "--virtual-time-budget=%d" % budget, "--window-size=%d,1200" % width,
             "--user-data-dir=" + os.path.join(tmpdir, "prof"), "--dump-dom", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        dom = p.stdout or ""
        m = re.search(r'<pre id="__rendered">(.*?)</pre>', dom, re.S)
        if not m:
            raise RuntimeError("探针未执行（页面 JS 可能在早期抛错）。stderr 尾部：\n"
                               + (p.stderr or "")[-500:])
        return json.loads(_html.unescape(m.group(1)))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    # Windows 控制台默认 GBK，中文断言输出会乱码 → 强制 UTF-8
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    ap = argparse.ArgumentParser(description="渲染级文本导出 / 断言")
    ap.add_argument("html")
    ap.add_argument("--ids", default="", help="逗号分隔的容器 id（--rules 里的 id 会自动并入）")
    ap.add_argument("--rules", default=None, help="断言 JSON 文件（可选）")
    ap.add_argument("--width", type=int, default=1500)
    ap.add_argument("--log", default=None,
                    help="把完整报告以 UTF-8 写入该文件（Windows 控制台常为 GBK，"
                         "中文断言输出会乱码；用 --log 再读文件即可）")
    args = ap.parse_args()

    sink = []
    def out(s=""):
        print(s)
        sink.append(str(s))

    rules = None
    if args.rules:
        rules = json.loads(io.open(args.rules, encoding="utf-8").read())
        # ⚠️ 以 `_` 开头的键是**注释约定**（_usage/_note/_comment_xxx），不是容器 id。
        #    必须剔除，否则会被当成 id 去渲染 → 一律 __MISSING__ → 整份规则假失败。
        #    （本脚本第二次实盘踩到：加了 4 个说明性键，结果 4 项 FAIL、exit 1。）
        rules = {k: v for k, v in rules.items() if not k.startswith("_")}

    # ⚠️ rules 里出现的 id 必须一起渲染 —— 否则会误报「容器不存在」。
    #    （本脚本首次实盘即踩：tRecoPriceNoFac / tpSaveState 只在 rules 里，
    #      渲染字典里没有 → 假失败。）
    ids = [s.strip() for s in args.ids.split(",") if s.strip()]
    if rules:
        for k in rules:
            if k not in ids:
                ids.append(k)
    if not ids:
        ap.error("至少要有一个 id（--ids 或 --rules 提供）")

    texts = render_texts(args.html, ids, width=args.width)

    for k in ids:
        out("=" * 72)
        out("[%s]" % k)
        out(texts.get(k))
    out("=" * 72)

    if not rules:
        if args.log:
            io.open(args.log, 'w', encoding='utf-8').write('\n'.join(sink))
        return 0

    fails = []
    for cid, spec in rules.items():
        body = texts.get(cid, "__MISSING__")
        if body == "__MISSING__":
            fails.append("%s: 容器不存在（__MISSING__）" % cid)
            out("  FAIL %s: 容器不存在" % cid)
            continue
        for s in spec.get("must_contain", []):
            if s not in body:
                fails.append("%s: 缺少 %r" % (cid, s))
                out("  FAIL %s: 缺少 %r" % (cid, s))
            else:
                out("  OK   %s: 含 %r" % (cid, s))
        for s in spec.get("must_not_contain", []):
            if s in body:
                fails.append("%s: 不应出现 %r" % (cid, s))
                out("  FAIL %s: 不应出现 %r" % (cid, s))
            else:
                out("  OK   %s: 不含 %r" % (cid, s))
        for pat in spec.get("must_match", []):
            if not re.search(pat, body):
                fails.append("%s: 未匹配 /%s/" % (cid, pat))
                out("  FAIL %s: 未匹配 /%s/" % (cid, pat))
            else:
                out("  OK   %s: 匹配 /%s/" % (cid, pat))
        for pat in spec.get("must_not_match", []):
            if re.search(pat, body):
                fails.append("%s: 命中禁配 /%s/" % (cid, pat))
                out("  FAIL %s: 命中禁配 /%s/" % (cid, pat))
            else:
                out("  OK   %s: 未命中禁配 /%s/" % (cid, pat))

    out()

    def flush_log():
        if args.log:
            io.open(args.log, 'w', encoding='utf-8').write('\n'.join(sink))

    if fails:
        out("❌ 渲染级检查未通过（%d 项）—— 不可交付：" % len(fails))
        for f in fails:
            out("   × " + f)
        flush_log()
        return 1
    out("✅ 渲染级检查通过。")
    flush_log()
    return 0


if __name__ == "__main__":
    sys.exit(main())
