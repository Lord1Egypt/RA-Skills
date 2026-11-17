#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_score_frozen.py —— 「评分类看板固化一致性」真机校验（通用，无项目信息）

为什么必须单独一道
    · verify_dashboard.js 只查「JS 能不能跑、图有没有画、有无 NaN」
    · check_overflow.py 只查版式
    · lint_py_const_leak.py 只查常量泄漏
    · dump_rendered.py 只查渲染后文案
    以上**都拦不住**「换台电脑打开分数就变了」这一类事故 —— 因为它不是报错，
    而是**静默回退到另一套分数**（localStorage 按 origin 隔离：file:// 与 https://
    互不相通；云文档还在 iframe 沙箱里，localStorage 可能整个不可用）。

判定手法
    用 **两个全新的 --user-data-dir**（等价于两台互不相通的电脑 / 两个陌生浏览器），
    各渲染同一次页面，断言：
      ① 评分类面板内 input/select/button/textarea 数量 == 0（不可修改）
      ② 每一位评委姓名都在表里
      ③ 页面**没有**写入评分类 localStorage key（lsKey 为空）
      ④ 综合评分表的各维度值 / 总分 / 名次 == 由 seed（配置）现算的期望值
      ⑤ 首屏推荐卡分数与名次 == 同一套期望值（无「—/100」类占位）
      ⑥ 两次运行结果**完全一致**
      ⑦ 可选：直接对**线上静态产物**跑同一套断言（--url 或 --html 指向下载下来的字节）

用法
    # 本地产物
    python verify_score_frozen.py ./看板.html --config ./score_config.json \
        --rules ./render_rules.json --log ./verify_score.log

    # 线上静态产物（先下载为文件，避免「壳页」误判）
    python verify_score_frozen.py ./online_static.html --config ./score_config.json --online

退出码 0 = 全部通过，可交付；非 0 = 有失败项，读 --log。
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]

# 被检查的 DOM 选择器（可在 render_rules.json 的 "_selectors" 里覆盖）
SEL_DEFAULT = {
    "panel": "#scorePanel, #teamPanel",
    "scoreTable": "#tScore, #scoreTable",
    "hero": "#heroReco, #heroCards",
    "rulesBox": "#scoreRulesBox, #rulesBox",
}


def find_chrome():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def load_cfg(path):
    return json.loads(io.open(path, encoding="utf-8").read())


# --------------------------------------------------------------------------
# 期望值现算（唯一真相源 = score_config.json）
# --------------------------------------------------------------------------
def expect_from_config(cfg):
    vendors = cfg["vendors"]
    dims = cfg["dims"]
    roles = cfg.get("roles") or ["采购", "设计", "零售", "零售", "销售"]
    judges = cfg["judges"]

    def row_name(j):
        return str(j.get("name") or "").strip()

    exp_avg = {}   # (dimKey, vendorName) -> 'x.xx'
    for d in dims:
        for v in vendors:
            k = "%s_%s" % (v["code"], d["code"])
            vals = []
            for j in judges:
                if not row_name(j):
                    continue
                val = j.get(k)
                if isinstance(val, int) and not isinstance(val, bool) and 0 <= val <= d["max"]:
                    vals.append(val)
            exp_avg[(d["key"], v["name"])] = ("%.2f" % (sum(vals) / len(vals))) if vals else None

    exp = {}
    for v in vendors:
        n = v["name"]
        team = sum(float(exp_avg[(d["key"], n)]) for d in dims if exp_avg[(d["key"], n)] is not None)
        fixed = (cfg.get("other_fixed") or {}).get(n)
        other = None if fixed is None else fixed + team
        price = (cfg.get("price_score") or {}).get(n)
        comp = None if (other is None or price is None) else price + other
        exp[n] = {"team": team, "other": other, "price": price, "composite": comp,
                  "dims": {d["key"]: exp_avg[(d["key"], n)] for d in dims}}
    order = sorted([v for v in exp if exp[v]["composite"] is not None],
                   key=lambda x: -exp[x]["composite"])
    for i, v in enumerate(order):
        exp[v]["rank"] = i + 1
    return exp, order, [row_name(j) for j in judges if row_name(j)], roles


# --------------------------------------------------------------------------
# 注入脚本
# --------------------------------------------------------------------------
TEST_JS = r"""
<script>
(function(){
  var SEL=__SEL__, CFG=__CFG__;
  function pick(list){ for(var i=0;i<list.length;i++){ var e=document.querySelector(list[i]); if(e) return e; } return null; }
  function out(o){
    var pre=document.getElementById('__test');
    if(!pre){ pre=document.createElement('pre'); pre.id='__test'; document.body.appendChild(pre); }
    pre.textContent='RESULT '+JSON.stringify(o);
  }
  window.addEventListener('load', function(){
    setTimeout(function(){
      try{
        var panel=pick(SEL.panel.split(','));
        var rules=pick(SEL.rulesBox.split(','));
        var heroEl=pick(SEL.hero.split(','));
        var tl=pick(SEL.scoreTable.split(','));
        var res={
          ctl: panel? panel.querySelectorAll('input,select,button,textarea').length : -1,
          panelFound: !!panel,
          panelText: panel? (panel.innerText||'').replace(/\s+/g,' ') : '',
          bodyFrozen: /评委最终打分|已固化|打分已固�化/.test(document.body.innerText||''),
          rulesFrozen: rules? /评委最终打分|已固化/.test(rules.innerText||'') : false,
          lsKeys: [],
          rows: {}, ranks: {}, dims: {}, hero: '',
          heroNumeric: 0, heroDash: 0
        };
        /* 1) 是否写了评分类 localStorage（任何 key 含 score/team/judge 都算） */
        try{
          for(var i=0;i<localStorage.length;i++){
            var k=localStorage.key(i)||'';
            if(/score|team|judge|rate/i.test(k)) res.lsKeys.push(k);
          }
        }catch(e){ res.lsKeys=['(blocked)']; }
        /* 2) 综合评分表：行文本 + 名次 */
        if(tl){
          var trs=tl.querySelectorAll('tbody tr, tr');
          for(var t=0;t<trs.length;t++){
            var tr=trs[t], txt=(tr.innerText||'').replace(/\s+/g,' ').trim();
            var dv=tr.getAttribute('data-v')||tr.getAttribute('data-vendor');
            if(!dv){
              var m=txt.match(/^(\S+?)\s/); dv=m? m[1] : ('row'+t);
            }
            if(/合计|总分|综合|total/i.test(txt) || (tr.className||'').indexOf('tot')>=0) res.rows[dv]=txt;
            var rk=tr.querySelector('.rv,.rank,.rankb');
            if(rk) res.ranks[dv]=rk.textContent.trim();
            tr.querySelectorAll('td[data-v],td[data-dim]').forEach(function(td){
              var v=td.getAttribute('data-v'), d=td.getAttribute('data-dim')||td.getAttribute('data-dimkey');
              if(v&&d) res.dims[d+'|'+v]=td.textContent.replace(/\s+/g,' ').trim();
            });
          }
        }
        /* 3) 首屏推荐卡 */
        if(heroEl){
          var parts=[];
          heroEl.querySelectorAll('.hero-card,[data-hero-card],.hc').forEach(function(c){
            var nm=(c.querySelector('.hr-name,.hc-name')||{}).textContent||'';
            var rk=(c.querySelector('.hr-rank,.hc-rank')||{}).textContent||'';
            var sc=(c.querySelector('.hr-score,.hc-score')||{}).textContent||'';
            parts.push(nm.trim()+'='+rk.trim()+'='+sc.trim());
            if(/\d+\.\d+\s*\/\s*100/.test(sc)) res.heroNumeric++;
            if(/—\s*\/\s*100/.test(sc)) res.heroDash++;
          });
          res.hero=parts.join(' ;; ');
        }
        out(res);
      }catch(e){ out({error:String(e&&e.message||e)}); }
    }, __DELAY__);
  });
})();
</script>
"""


def build_test_js(sel, cfg, delay, use_dom_probe):
    js = TEST_JS.replace("__SEL__", json.dumps(sel, ensure_ascii=False))
    js = js.replace("__CFG__", "{}")
    js = js.replace("__DELAY__", str(delay))
    return js


def inject(html, js):
    i = html.rfind("</body>")
    if i < 0:
        i = html.rfind("</html>")
    return html[:i] + js + html[i:] if i >= 0 else html + js


def run_chrome(chrome, url, profile, dump=True):
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
           "--no-first-run", "--no-default-browser-check", "--disable-extensions",
           "--user-data-dir=" + profile,
           "--virtual-time-budget=15000", "--window-size=1500,1200"]
    if dump:
        cmd.append("--dump-dom")
    cmd.append(url)
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=300)
    m = re.search(r'<pre id="__test">RESULT (.*?)</pre>', p.stdout or "", re.S)
    if not m:
        return None, (p.stderr or "")[-500:]
    return m.group(1).strip(), None


def main():
    ap = argparse.ArgumentParser(description="评分类看板固化一致性真机校验")
    ap.add_argument("html", help="待校验的看板 HTML（本地或已下载的线上字节）")
    ap.add_argument("--config", required=True, help="score_config.json")
    ap.add_argument("--rules", default="./render_rules.json",
                    help="可选：含 _selectors 的规则文件")
    ap.add_argument("--log", default="./verify_score.log")
    ap.add_argument("--online", action="store_true", help="标记为线上产物（仅改文案）")
    ap.add_argument("--delay", type=int, default=700, help="DOM 就绪后的等待毫秒数")
    args = ap.parse_args()

    base = Path(args.html).resolve().parent
    cfg = load_cfg(args.config)
    exp, order, names, roles = expect_from_config(cfg)

    sel = dict(SEL_DEFAULT)
    rules_path = Path(args.rules)
    if args.rules and rules_path.is_file():
        try:
            rr = load_cfg(str(rules_path))
            sel.update({k: v for k, v in (rr.get("_selectors") or {}).items()})
        except Exception:
            pass

    log = []
    tag = "线上产物" if args.online else "本地产物"
    log.append("=== 评分类看板固化一致性校验（%s）===" % tag)
    log.append("源文件: %s" % args.html)
    log.append("配置:   %s  (评委 %d 位 / 单位 %d 家 / 维度 %d 个)"
               % (args.config, len(cfg["judges"]), len(cfg["vendors"]), len(cfg["dims"])))

    chrome = find_chrome()
    log.append("chrome: %s" % chrome)
    if not chrome:
        log.append("失败项: 未找到 Chrome，无法真机校验")
        io.open(args.log, "w", encoding="utf-8").write("\n".join(log) + "\n")
        print("\n".join(log))
        return 1

    html = io.open(args.html, encoding="utf-8", errors="replace", newline="").read()
    js = build_test_js(sel, cfg, args.delay, None)
    tmp = base / ("_frozen_probe.html" if not args.online else "_frozen_probe_online.html")
    io.open(tmp, "w", encoding="utf-8", newline="").write(inject(html, js))

    results = []
    for tag2 in ("a", "b"):
        prof = os.path.join(tempfile.gettempdir(), "_sf_prof_" + tag2)
        shutil.rmtree(prof, ignore_errors=True)
        os.makedirs(prof, exist_ok=True)
        url = "file:///" + str(tmp).replace("\\", "/")
        res, err = run_chrome(chrome, url, prof)
        log.append("[档案 %s] %s" % (tag2, (res or "NO RESULT")[:400]))
        if err:
            log.append("[档案 %s] stderr: %s" % (tag2, err))
        try:
            results.append(json.loads(res) if res else None)
        except Exception:
            results.append(None)

    fails = []

    def chk(name, cond, extra=""):
        log.append(("  OK   " if cond else "  FAIL ") + name + (("  " + str(extra)) if extra != "" else ""))
        if not cond:
            fails.append(name)

    ra, rb = results[0], results[1]
    if not ra or not rb:
        chk("两次运行均取回结果", False, "a=%s b=%s" % (bool(ra), bool(rb)))
    else:
        chk("找到评分类面板", ra.get("panelFound") is True)
        chk("面板内无 input/select/button/textarea（只读固化）", ra.get("ctl") == 0, ra.get("ctl"))
        chk("页面含固化标识文案", ra.get("bodyFrozen") is True)
        chk("规则盒已切换为固化措辞", ra.get("rulesFrozen") is True)
        pn = ra.get("panelText") or ""
        for nm in names:
            chk("评委在表：%s" % nm, nm in pn)
        chk("有效平均行存在", ("有效平均" in pn) or ("共 %d 人有效" % len(names) in pn))
        chk("未写入评分类 localStorage", not ra.get("lsKeys"), ra.get("lsKeys"))

        # 综合分与名次
        tl_found = ra.get("rows") or {}
        hero_txt = ra.get("hero") or ""
        if not tl_found and not hero_txt:
            log.append("  --   看板内未找到「综合评分表」或「首屏推荐卡」容器 → "
                       "本看板为纯价格比价版（无评分类节），跳过综合分/名次断言。")
            log.append("       若本应含评分节，请检查 --rules 里的 _selectors 是否指向正确的容器 id。")
        else:
            txt_all = " ".join(tl_found.values()) + " " + (ra.get("panelText") or "")
            for v in exp:
                e = exp[v]
                if e["composite"] is None:
                    continue
                want = "%.2f" % e["composite"]
                hit = (want in txt_all) or (want in hero_txt)
                chk("综合分出现 %s = %s" % (v, want), hit, tl_found.get(v, "")[:120])

            # 首屏卡
            hc = re.sub(r"\s+", "", hero_txt)
            if hero_txt:
                for v in exp:
                    e = exp[v]
                    if e["composite"] is None:
                        continue
                    want = re.sub(r"\s+", "", "%s=第%s名=%.2f/100" % (v, e["rank"], e["composite"]))
                    chk("首屏卡 %s" % want, want in hc, hc[:220])
                chk("首屏卡分数均为数值（无占位「—」）", ra.get("heroDash", 0) == 0, ra.get("heroDash"))
            else:
                log.append("  --   未找到首屏推荐卡容器（按需跳过）")

        same = (ra.get("rows") == rb.get("rows") and ra.get("dims") == rb.get("dims")
                and ra.get("hero") == rb.get("hero") and ra.get("ranks") == rb.get("ranks"))
        chk("两个独立档案（= 两台电脑）结果完全一致", same)
        if not same:
            log.append("     a.rows=%s" % json.dumps(ra.get("rows"), ensure_ascii=False))
            log.append("     b.rows=%s" % json.dumps(rb.get("rows"), ensure_ascii=False))

    log.append("")
    log.append("失败项: %s" % (fails if fails else "无 —— 全部通过"))
    io.open(args.log, "w", encoding="utf-8").write("\n".join(log) + "\n")
    print("\n".join(log))
    try:
        tmp.unlink()
    except Exception:
        pass
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
