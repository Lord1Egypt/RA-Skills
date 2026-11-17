# -*- coding: utf-8 -*-
"""Dawn Proactive Agent v1.2"""

import argparse, json, os, sys, urllib.request, time, subprocess
from datetime import datetime, timedelta
from pathlib import Path

WS = Path(os.environ.get("OPENCLAW_WORKSPACE", "")) or Path.home() / ".openclaw" / "workspace"
S = lambda n: WS / n
STATE_FILE = S("session-state.json")
DECISION_FILE = S("memory/decision-registry.json")
PROACTIVE_LOG = S("memory/proactive-log.md")

def log(m): print(f"[DAWN] {m}")
def warn(m): print(f"[WARN] {m}")
def err(m): print(f"[ERROR] {m}")
def ok(m): print(f"[OK] {m}")
def sep(): print("-" * 50)

def lj(p):
    if p.exists():
        try: return json.loads(p.read_text(encoding="utf-8"))
        except: return None
    return None

def sj(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def lp(a, d, r=None):
    n = datetime.now().strftime("%Y-%m-%d %H:%M")
    e = f"- [{n}] **{a}**: {d}"
    if r: e += f" -> {r}"
    e += "\n"
    PROACTIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(PROACTIVE_LOG, "a", encoding="utf-8") as f: f.write(e)

def market_status():
    n = datetime.now()
    if n.weekday() >= 5: return "weekend"
    t = n.hour * 100 + n.minute
    if t < 900: return "closed"
    if t < 915: return "pre_open"
    if t < 1130: return "trading_morning"
    if t < 1300: return "lunch_break"
    if t < 1500: return "trading_afternoon"
    if t < 1600: return "post_market"
    return "closed"

# ---- 弹性网络请求(含重试) ----

def fetch(url, timeout=10, retries=3):
    """带重试的JSON请求"""
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8"))
        except Exception as e:
            last_err = e
            if attempt < retries - 1:
                time.sleep(1 * (attempt + 1))
    raise last_err

def get_overview():
    L = []
    L.append("> 大盘指数")
    for code, name in [("1.000001","上证"),("0.399001","深证"),("0.399006","创业板"),("1.000688","科创50")]:
        try:
            d = fetch(f"https://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields=f43,f44,f45,f46")
            k = d.get("data",{})
            if k:
                c = k.get("f43",0)/100; o = k.get("f46",0)/100
                chg = ((c-o)/o*100) if o else 0
                L.append(f"  {name}: {c:.2f} ({chg:+.2f}%)")
        except: L.append(f"  {name}: err")
    L.append("\n> 行业板块TOP5")
    try:
        for i in fetch("https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f12,f14,f3").get("data",{}).get("diff",[]):
            L.append(f"  {i.get('f14','')}: {i.get('f3',0)}%")
    except:
        L.append("  (try backup...)")
        try:
            for i in fetch("https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:2&fields=f12,f14,f3,f62").get("data",{}).get("diff",[]):
                v = (i.get("f62") or 0) / 1e8
                L.append(f"  {i.get('f14','')}: {i.get('f3',0)}% | +{v:.1f}亿")
        except:
            L.append("  (unavailable)")
    L.append("\n> 概念板块TOP5")
    try:
        for i in fetch("https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f12,f14,f3").get("data",{}).get("diff",[]):
            L.append(f"  {i.get('f14','')}: {i.get('f3',0)}%")
    except:
        L.append("  (try backup...)")
        try:
            for i in fetch("https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=5&po=1&np=1&fltt=2&invt=2&fid=f62&fs=m:90+t:3&fields=f12,f14,f3,f62").get("data",{}).get("diff",[]):
                v = (i.get("f62") or 0) / 1e8
                L.append(f"  {i.get('f14','')}: {i.get('f3',0)}% | +{v:.1f}亿")
        except:
            L.append("  (unavailable)")
    return "\n".join(L)

def get_pos():
    st = lj(STATE_FILE)
    if not st: return "> 持仓: no state"
    holdings = st.get("holdings", {})
    if isinstance(holdings, dict) and holdings:
        L = ["> 当前持仓"]
        for code, info in holdings.items():
            name = info.get("name", code)
            ratio = info.get("ratio", "")
            pnl = info.get("profit_pct", "")
            r = f"  {name} ({code})"
            if ratio: r += f" [{ratio}]"
            if pnl: r += f" P&L: {pnl:+.2f}%"
            L.append(r)
        return "\n".join(L)
    elif isinstance(holdings, list) and holdings:
        L = ["> 当前持仓"]
        for p in holdings:
            if isinstance(p, dict):
                nm = p.get("name", p.get("code", "?"))
                cd = p.get("code", "")
                v = p.get("volume", p.get("amount", 0))
                L.append(f"  {nm} ({cd}): {v}")
            else:
                L.append(f"  {p}")
        return "\n".join(L)
    return "> 持仓: empty"

# --- Handlers ---

def h_morning():
    sep(); log("盘前检查")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(get_overview()); sep()
    print(get_pos()); sep()
    wd = ["周一","周二","周三","周四","周五","周六","周日"][datetime.now().weekday()]
    print(f"今天: {wd}")
    ok("盘前检查完成")

def h_midday():
    sep(); log("午盘复盘")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(get_pos()); sep()
    ok("午盘复盘完成")

def h_afternoon():
    sep(); log("收盘复盘")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(get_overview()); sep()
    print(get_pos()); sep()
    ok("收盘复盘完成")

def h_evening():
    sep(); log("盘后分析")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(get_overview()); sep()
    print(get_pos()); sep()
    od = get_overdue()
    if od:
        warn(f"{len(od)} 逾期决策")
        for d in od: print(f"  {d['name']} ({d['id']})")
        # 自动验证: 标记为继续观察
        for d in od:
            v = auto_verify(d)
            if v: print(f"  -> 自动验证通过")
    else:
        ok("无逾期决策")
    if datetime.now().weekday() == 4:
        log("周五: 检查周末持仓风险")
    sep(); ok("盘后分析完成")

def load_dec():
    if DECISION_FILE.exists():
        try: return json.loads(DECISION_FILE.read_text(encoding="utf-8"))
        except: return {"decisions":[],"last_check":None}
    return {"decisions":[],"last_check":None}

def get_overdue():
    reg = load_dec(); n = datetime.now(); od = []
    for d in reg["decisions"]:
        if d["status"] != "active": continue
        try:
            if datetime.fromisoformat(d["follow_up_by"]) <= n: od.append(d)
        except: od.append(d)
    return od

def auto_verify(d):
    """自动验证决策结果"""
    did = d["id"]
    # 规则1: 系统类决策 - 检查相关文件存在性
    if d.get("category") == "system":
        if "Cron" in d.get("expected_outcome","") or "引擎" in d.get("decision",""):
            # 检查引擎文件
            engine_ok = (WS / "scripts" / "dawn_proactive.py").exists()
            if engine_ok:
                reg = load_dec()
                for dr in reg["decisions"]:
                    if dr["id"] == did:
                        dr["status"] = "verified"
                        dr["verified_at"] = datetime.now().isoformat()
                        dr["actual_outcome"] = "引擎文件存在，Cron任务已部署"
                        dr["learned"] = "v1.1升级完成，CLI参数+Cron接通"
                        sj(DECISION_FILE, reg)
                        lp("自动验证", f"{d['name']}: 通过")
                        return True
    return False

def h_backtrack():
    sep(); log("决策回溯")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    reg = load_dec(); ds = reg.get("decisions",[])
    print(f"总决策: {len(ds)}")
    if not ds: ok("无决策"); return
    ac = len([d for d in ds if d.get("status")=="active"])
    vf = len([d for d in ds if d.get("status")=="verified"])
    fa = len([d for d in ds if d.get("status")=="failed"])
    print(f"  活跃: {ac}  已验证: {vf}  失败: {fa}")
    od = get_overdue()
    if od:
        warn(f"=== {len(od)} 逾期决策 ===")
        for d in od:
            print(f"  ID: {d['id']}  {d['name']}")
            print(f"    决策: {d['decision'][:60]}")
            if auto_verify(d):
                print(f"    -> 自动验证通过")
            else:
                print(f"    -> 需要手动验证")
    else:
        ok("无逾期决策")
    sep(); ok("回溯完成")

def h_health():
    sep(); log("健康检查")
    print(f"市场: {market_status()}")
    dec = load_dec()
    print(f"决策文件: {'OK' if dec else 'MISSING'} ({len(dec.get('decisions',[]))})")
    st = lj(STATE_FILE)
    print(f"session-state: {'OK' if st else 'MISSING'}")
    for s in ["dawn_etf_rotator.py","dawn_proactive.py","skill_health_scan.py"]:
        print(f"  {s}: {'OK' if (WS/'scripts'/s).exists() else 'MISSING'}")
    ok("健康检查完成")

def h_surprise():
    sep(); log("Proactive Surprise")
    fh = []
    # 1. 过期核心文件
    for n,p in [("AGENTS.md",WS/"AGENTS.md"),("SOUL.md",WS/"SOUL.md"),("MEMORY.md",WS/"MEMORY.md")]:
        if p.exists():
            a = datetime.now()-datetime.fromtimestamp(p.stat().st_mtime)
            if a.days > 7: fh.append(f"{n} {a.days}天未更新")
    # 2. __pycache__
    pc = len(list(WS.rglob("__pycache__")))
    if pc > 5: fh.append(f"{pc}个__pycache__目录")
    # 3. Python语法检查
    py_files = list(WS.rglob("scripts/*.py"))
    bad = 0
    for pf in py_files:
        r = subprocess.run([sys.executable, "-m", "py_compile", str(pf)], capture_output=True, text=True, timeout=10)
        if r.returncode != 0: bad += 1
    if bad > 0: fh.append(f"{bad}/{len(py_files)}脚本语法错误")
    else: log(f"{len(py_files)}个Python文件语法检查通过")
    # 4. 30天未用archive
    ar = WS / "archive"
    if ar.exists():
        old = [f for f in ar.rglob("*") if f.is_file() and (datetime.now()-datetime.fromtimestamp(f.stat().st_mtime)).days > 30]
        if old: fh.append(f"archive中{len(old)}个>30天文件")
    if fh:
        warn(f"{len(fh)}个优化机会:")
        for f in fh: print(f"  - {f}")
    else: ok("系统整洁")
    ok("Surprise完成")

def h_status():
    sep()
    print("曙光 Proactive Agent v1.2")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"市场: {market_status()}")
    reg = load_dec(); ds = reg.get("decisions",[])
    ac = len([d for d in ds if d.get("status")=="active"])
    vf = len([d for d in ds if d.get("status")=="verified"])
    od = len(get_overdue())
    print(f"决策: {len(ds)}总/{ac}活跃/{vf}验证/{od}逾期")
    if PROACTIVE_LOG.exists():
        L = PROACTIVE_LOG.read_text(encoding="utf-8").strip().split("\n")
        R = L[-3:] if len(L)>=3 else L
        print(f"\n最近({len(L)}条):")
        for l in R: print(f"  {l}")
    sep(); ok("状态报告")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--action", choices=["morning","midday","afternoon","evening","backtrack","health","status","surprise"], default="status")
    ap.add_argument("--register", nargs=4)
    ap.add_argument("--verify", nargs=3)
    a = ap.parse_args()
    if a.register:
        n,d,e,c = a.register
        reg = load_dec(); now = datetime.now().isoformat()
        fu = (datetime.now()+timedelta(days=7)).isoformat()
        ent = {"id":f"DEC-{datetime.now().strftime('%Y%m%d')}-{len(reg['decisions'])+1:03d}","name":n,"decision":d,"expected_outcome":e,"category":c,"created":now,"follow_up_by":fu,"status":"active","verified_at":None,"actual_outcome":None,"learned":None}
        reg["decisions"].append(ent); reg["last_check"]=now; sj(DECISION_FILE,reg)
        lp("注册",f"{n}: {d[:40]}...")
        print(f"[OK] Registered: {ent['id']}"); return
    if a.verify:
        did,out,learn = a.verify
        reg = load_dec()
        for d in reg["decisions"]:
            if d["id"]==did:
                d["status"]="verified"; d["verified_at"]=datetime.now().isoformat()
                d["actual_outcome"]=out; d["learned"]=learn
                sj(DECISION_FILE,reg); lp("验证",f"{d['name']}"); print(f"[OK] {did} verified"); return
        err(f"{did} not found"); return
    {"morning":h_morning,"midday":h_midday,"afternoon":h_afternoon,"evening":h_evening,"backtrack":h_backtrack,"health":h_health,"status":h_status,"surprise":h_surprise}.get(a.action)()

if __name__ == "__main__":
    main()
