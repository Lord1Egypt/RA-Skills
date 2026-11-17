# -*- coding: utf-8 -*-
"""看板横向溢出体检（浏览器实测，非静态推断）。

用途：verify_dashboard.js 只验证「JS 能跑、图能画、无 NaN」，**看不见版式溢出**。
      本脚本用 headless Chrome 实测 DOM 盒模型，抓出「内容超出页面/卡片范围」的 bug
      —— 典型成因是 CSS 里 `td{white-space:nowrap}` 让长文本列（法规依据、描述译文、
      条款原文等）拒绝换行，把整张表撑出卡片边界，页面上表现为内容溢出到页面外、
      右侧出现大片空白/横向滚动条。

三个指标，语义不同，别混用：
  · PAGE_SCROLL   = 页面级横向滚动（doc.scrollWidth - doc.clientWidth）→ 致命，必须为 0；
                    这是「内容超出页面范围」最直接的判据，出现横向滚动条即命中
  · BEYOND_WRAP   = 内容**视觉上**超出 .wrap 右边界（已按祖先 overflow 裁切折算）→ 致命，必须为 0；
                    用于捕获「页面不滚但内容被切掉」的情形
  · SCROLLABLE    = 某容器内部存在横向滚动（scrollWidth > clientWidth）→ 信息项；
                    若该容器本就是 overflow-x:auto 的宽表兜底，属正常；若无意为之则收窄列宽

  ⚠️ 计算 BEYOND_WRAP 必须先把祖先的 overflow 裁切折算进去：
     getBoundingClientRect() 返回的是布局盒、不理会祖先 overflow，
     直接拿它比 wrapRight 会把一个正常的「overflow-x:auto 宽表」误判成页面级溢出（假警报）。
  ⚠️ 反过来，只靠 BEYOND_WRAP 会**漏报**：若沿途有 overflow:hidden 的祖先把内容裁掉，
     BEYOND_WRAP 会被折算成 0，而文档其实已经横向滚动了 —— 所以必须同时看 PAGE_SCROLL。

用法：
    python check_overflow.py <看板.html> [宽度1,宽度2,...]        # 默认 1500,1280,1100
    python check_overflow.py <看板.html> --strict                # 连 SCROLLABLE 也当失败
    python check_overflow.py <看板.html> --before "<CSS片段>"     # 正对照：置空该规则自证检测有效
                                                                 # （通常传「裁剪/滚动兜底」那条）

退出码：0 = 无页面级溢出（可交付）；1 = 存在页面级溢出（不可交付）；2 = 用法/环境问题。
"""
import io
import os
import re
import subprocess
import sys
import tempfile

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

MEASURE_JS = """
<script>
(function(){
  var doc = document.documentElement, wrap = document.querySelector('.wrap') || document.body;
  var wrapRight = wrap.getBoundingClientRect().right;
  var sel = '.sec, .tblscroll, .tp-tablewrap, .tablewrap, table, .mstrip, .vgrid, .twinrow';
  var over = [];
  document.querySelectorAll(sel).forEach(function(el){
    if (el.scrollWidth - el.clientWidth > 1)
      over.push((el.tagName+'.'+(el.className||'')).slice(0,44)+' sw='+el.scrollWidth+' cw='+el.clientWidth);
  });

  // 元素被最近的「滚动/裁剪祖先」裁切后的可见右边界。
  // 必须做这一步：getBoundingClientRect() 返回布局盒，不理会祖先 overflow，
  // 直接用它会把一个正常的 overflow-x:auto 宽表误判成页面级溢出（假警报）。
  function clips(cs){
    var ox = cs.overflowX;
    return ox === 'auto' || ox === 'scroll' || ox === 'hidden' || ox === 'clip';
  }
  function visibleRight(el){
    var r = el.getBoundingClientRect().right;
    var p = el.parentElement;
    while (p){
      if (clips(getComputedStyle(p))){
        var pr = p.getBoundingClientRect().right;
        if (r > pr) r = pr;
      }
      if (p === wrap) break;
      p = p.parentElement;
    }
    return r;
  }

  var bad = [];
  document.querySelectorAll('.wrap *').forEach(function(el){
    var r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return;
    var vr = visibleRight(el);
    if (vr > wrapRight + 1)
      bad.push((el.tagName+'.'+(el.className||'')).slice(0,44)+' right='+Math.round(vr));
  });

  // ── CLIPPED：内容被「人为高度上限」藏起来（不是横向溢出，但同样是交付事故）──
  // 典型：全局 `.tblwrap{max-height:420px;overflow-y:auto}` 遇到超高表格，
  //   把最后几行（往往正是"合计/综合总分"行）裁进内部滚动区 →
  //   截图和打印都看不到，而且表格盒高 > 容器高，后随元素会压在那片溢出区上，
  //   看上去像"文字重叠"。（2026-09-16 某门店评分表实测：489px 内容 / 420px 上限，
  //   隐藏的正是最关键的「综合总分（100 分）」行。）
  // 判定只看「显式设了 max-height 且内容更高」——设计上的滚动区（overflow:auto
  //   且无 max-height，如 min-width 撑宽的宽表）不算，避免误报。
  var clipped = [];
  document.querySelectorAll('.wrap *').forEach(function(el){
    var cs = getComputedStyle(el);
    if (cs.maxHeight === 'none' || cs.display === 'none') return;
    var gapH = el.scrollHeight - el.clientHeight;
    if (gapH > 8 && el.clientHeight > 0)
      clipped.push((el.tagName+'.'+(el.className||'')).slice(0,40)
                   +' hidden='+gapH+'px maxH='+cs.maxHeight
                   +' ids='+(el.id||(el.firstElementChild&&el.firstElementChild.id)||'-'));
  });

  var out = 'RESULT|docScrollW='+doc.scrollWidth+'|docClientW='+doc.clientWidth
          + '|PAGE_SCROLL='+Math.max(0, doc.scrollWidth - doc.clientWidth)
          + '|wrapRight='+Math.round(wrapRight)+'|SCROLLABLE='+over.length+'|BEYOND_WRAP='+bad.length
          + '|CLIPPED='+clipped.length;
  if(over.length) out += ' ||SCROLL: '+over.slice(0,8).join('  ;;  ');
  if(bad.length)  out += ' ||BAD: '+bad.slice(0,8).join('  ;;  ');
  if(clipped.length) out += ' ||CLIP: '+clipped.slice(0,8).join('  ;;  ');
  var pre=document.createElement('pre'); pre.id='__measure'; pre.textContent=out;
  pre.style.position='fixed'; pre.style.left='0'; pre.style.top='0';
  pre.style.whiteSpace='pre-wrap'; pre.style.wordBreak='break-all'; pre.style.zIndex='-1';
  document.body.appendChild(pre);
})();
</script>
"""


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def inject(html, js):
    """把测量脚本插到【最后】一个 </body> 之前。

    ⚠️ 不能用 replace("</body>", ...)：echarts 压缩代码里含字面量 '</body>'，
       replace 会命中第一个（在 JS 字符串内部），脚本永不执行 → 报 NO_RESULT。
    """
    i = html.rfind("</body>")
    if i < 0:
        i = html.rfind("</html>")
    if i < 0:
        return html + js
    return html[:i] + js + html[i:]


def measure(chrome, path, width):
    url = "file:///" + os.path.abspath(path).replace("\\", "/")
    p = subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--virtual-time-budget=6000", "--window-size=%d,1200" % width, "--dump-dom", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r'<pre id="__measure"[^>]*>(.*?)</pre>', p.stdout or "", re.S)
    if not m:
        return None, (p.stderr or "")[-200:]
    return m.group(1).strip(), None


def parse(res):
    d = {}
    for kv in res.split("||")[0].split("|")[1:]:
        if "=" in kv:
            k, v = kv.split("=", 1)
            d[k] = v
    return d


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__)
        return 2

    before_css = []
    while "--before" in args:
        i = args.index("--before")
        if i + 1 < len(args):
            before_css.append(args[i + 1])
        del args[i:i + 2]

    strict = "--strict" in args
    if strict:
        args.remove("--strict")

    src = args[0]
    widths = [int(x) for x in (args[1] if len(args) > 1 else "1500,1280,1100").split(",")]

    if not os.path.exists(src):
        print("找不到文件：%s" % src)
        return 2
    chrome = find_chrome()
    if not chrome:
        print("找不到 Chrome，无法做浏览器实测（可改用人工目视检查）")
        return 2

    html = io.open(src, encoding="utf-8").read()
    tmp = tempfile.mkdtemp(prefix="cockpit_overflow_")
    cases = [("after.html", inject(html, MEASURE_JS), "【当前 CSS】")]
    hit = [s for s in before_css if s in html]
    if hit:
        # 正对照：把指定 CSS 规则逐条置空，用以证明检测手段确实抓得住真实的页面级溢出。
        # 复现「原缺陷」通常要同时置空两条：① 裁剪/滚动兜底（如 .tblscroll{overflow-x:auto}）
        # ② 长文本换行规则（table.fixed td{white-space:normal;...}）→ 二者齐失才会真的撑破页面。
        b = html
        for s in hit:
            b = b.replace(s, s.split("{")[0] + "{}")
        cases.insert(0, ("before.html", inject(b, MEASURE_JS),
                         "【对照·置空 %d 条规则】" % len(hit)))
    elif before_css:
        print("⚠️  给定的 --before 片段在 HTML 中未找到，已跳过正对照\n")

    fatal = 0
    warn = 0
    clipped = 0
    ctl_fatal = 0
    ctl_seen = False
    for fname, h, label in cases:
        io.open(os.path.join(tmp, fname), "w", encoding="utf-8").write(h)

    for w in widths:
        print("=" * 100)
        print("视窗宽度 = %d px" % w)
        print("=" * 100)
        for fname, _h, label in cases:
            res, err = measure(chrome, os.path.join(tmp, fname), w)
            if res is None:
                print("  %s NO_RESULT  (%s)" % (label, err))
                if fname == "after.html":
                    fatal += 1
                continue
            d = parse(res)
            sc = int(d.get("SCROLLABLE", "0") or 0)
            bw = int(d.get("BEYOND_WRAP", "0") or 0)
            ps = int(d.get("PAGE_SCROLL", "0") or 0)
            cl = int(d.get("CLIPPED", "0") or 0)
            print("  %s PAGE_SCROLL=%s  BEYOND_WRAP=%s  CLIPPED=%s  SCROLLABLE=%s  docScrollW=%s docClientW=%s"
                  % (label, d.get("PAGE_SCROLL"), d.get("BEYOND_WRAP"), d.get("CLIPPED"),
                     d.get("SCROLLABLE"), d.get("docScrollW"), d.get("docClientW")))
            detail = res.split("||", 1)
            if len(detail) > 1:
                print("      %s" % detail[1].strip())
            if fname == "after.html":
                if bw or ps:
                    fatal += 1
                if cl:
                    clipped += 1
                if sc:
                    warn += 1
            else:
                ctl_seen = True
                if bw or ps:
                    ctl_fatal += 1
        print()

    print("-" * 100)
    if ctl_seen:
        if ctl_fatal:
            print("✔ 正对照有效：置空指定规则后复现了页面级横向溢出（PAGE_SCROLL>0），"
                  "证明本检测手段确实抓得住该缺陷。")
        else:
            print("⚠️  正对照未复现溢出——说明置空的规则不是该页溢出的成因，"
                  "或该页当前本就没有此类溢出；请核对 --before 应传的规则。")
    if warn:
        print("ℹ️  有 %d 处容器内部存在横向滚动（SCROLLABLE>0）——内容仍可横向滚动看到，"
              "不属页面级溢出；若是无意为之（如表被 min-width 撑宽），考虑收窄列宽去掉横滚。" % warn)
    if clipped:
        print("❌ 有 %d 处内容被「人为高度上限」藏起来了（CLIPPED>0）——凡设了 max-height "
              "且内容更高的容器，多出来的部分只有滚动才能看到，截图与打印一律丢失。"
              "本次命中项见上方 CLIP: 明细。典型受害行是「合计 / 综合总分」——"
              "那是表格最关键的一行，被裁掉却「看起来只是排版紧」。"
              "修法：给该容器解除高度上限（如新增 .tblwrap-tall{max-height:none}）或压缩行高。\n"
              % clipped)
    if fatal or (strict and warn) or clipped:
        if fatal:
            print("❌ 存在页面级横向溢出（PAGE_SCROLL 或 BEYOND_WRAP > 0），不可交付。"
                  "检查长文本列是否被 nowrap 撑破：给表格加 table-layout:fixed + <colgroup> 控列宽，"
                  "并让长文本列 white-space:normal;word-break:break-word;overflow-wrap:anywhere。")
        elif clipped:
            print("❌ 不可交付：存在被高度上限裁切的内容（CLIPPED>0，详见上方说明）。")
        else:
            print("❌ 不可交付（--strict）：容器内部横滚被视为失败。")
        return 1
    print("✅ 无页面级横向溢出，且无被高度上限裁切的内容。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
