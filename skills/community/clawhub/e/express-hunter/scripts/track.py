"""
快递单号查询脚本 - 聚合数据（主）+ 快递100（备）
用法: python track.py <快递单号>
"""
import sys, json, urllib.request, urllib.parse, os
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

DATA_DIR = "G:/PC先生/express_data"
PACKAGES_FILE = os.path.join(DATA_DIR, "packages.json")
# 从桌面文件读取 Key（方便更新）
_key_file = os.path.join(os.environ.get("USERPROFILE",""), "Desktop", "999.txt")
try:
    with open(_key_file, "r") as f:
        JUHE_KEY = f.read().strip()
except:
    JUHE_KEY = ""
JUHE_URL = "http://v.juhe.cn/exp/index"
KUAIDI100_URL = "https://www.kuaidi100.com/query"

COURIER_NAME_MAP = {
    "shunfeng": "顺丰速运", "yuantong": "圆通速递", "zhongtong": "中通快递",
    "shentong": "申通快递", "yunda": "韵达快递", "ems": "EMS",
    "jd": "京东物流", "jtexpress": "极兔速递", "debangwuliu": "德邦物流",
    "youzhengguonei": "邮政包裹", "youzhengbk": "邮政标快",
    "huitongkuaidi": "百世汇通", "tiantian": "天天快递",
    "youshuwuliu": "优速快递", "annengwuliu": "安能物流",
    "danniao": "丹鸟物流", "cainiao": "菜鸟裹裹",
}

def query_juhe(tn):
    """聚合数据查询 —— 主力"""
    params = urllib.parse.urlencode({"key": JUHE_KEY, "com": "auto", "no": tn.strip()})
    req = urllib.request.Request(f"{JUHE_URL}?{params}", headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None
    if data.get("resultcode") != "200" or data.get("error_code") != 0:
        return None
    r = data.get("result", {})
    courier_name = r.get("company", "未知")
    # 统一去除后缀再匹配
    cn_clean = courier_name.replace("快递","").replace("物流","").replace("速运","")
    code_map = {v.replace("快递","").replace("物流","").replace("速运",""): k for k, v in COURIER_NAME_MAP.items()}
    code = code_map.get(cn_clean, "unknown")
    # "自动匹配"或未识别时，从轨迹反推或前缀匹配
    if courier_name in ("自动匹配", "未知") or code == "unknown":
        tmp_traces = [{"context": t.get("remark","")} for t in r.get("list",[])]
        new_code, new_name = correct_courier(tmp_traces, code, "")
        if new_code != "unknown":
            code, courier_name = new_code, new_name
        else:
            # 回退：前缀检测
            prefix = detect_courier(tn)
            if prefix:
                code = prefix
                courier_name = COURIER_NAME_MAP.get(prefix, prefix)
    traces = [{"time": t.get("datetime",""), "context": t.get("remark","")} for t in r.get("list",[])]
    s = r.get("status","0")
    return {
        "success": True, "tracking_number": tn, "courier": courier_name,
        "courier_code": code, "status": "运输中" if s in ("0","1","2") else ("已签收" if s=="3" else "运输中"),
        "delivered": s == "3", "traces": traces, "trace_count": len(traces),
        "has_data": len(traces) > 0, "source": "juhe"
    }

def query_kuaidi100(tn, courier_type="auto"):
    """快递100回退"""
    params = urllib.parse.urlencode({"type": courier_type, "postid": tn.strip()})
    req = urllib.request.Request(f"{KUAIDI100_URL}?{params}", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"status": "error", "message": str(e)}

PREFIX_MAP = [("SF","shunfeng"),("YT","yuantong"),("YD","yunda"),("JT","jtexpress"),
    ("JD","jd"),("JDV","jd"),("JDX","jd"),("DP","debangwuliu"),("DPK","debangwuliu"),
    ("ZT","zhongtong"),("STO","shentong"),("EMS","ems"),("PH","ems")]

NUMERIC_FALLBACK = ["zhongtong","yuantong","shentong","yunda","jtexpress"]

TRACE_SIGNALS = {
    "中国邮政":"youzhengguonei","邮政":"youzhengguonei","EMS":"ems","顺丰":"shunfeng",
    "圆通":"yuantong","中通":"zhongtong","申通":"shentong","韵达":"yunda",
    "百世":"huitongkuaidi","极兔":"jtexpress","京东":"jd","德邦":"debangwuliu",
    "天天":"tiantian","宅急送":"zhaijisong","优速":"youshuwuliu","丹鸟":"danniao",
    "菜鸟":"cainiao","安能":"annengwuliu",
    "95554":"yuantong","95311":"zhongtong","95546":"shentong","95543":"huitongkuaidi",
    "956025":"jtexpress","11183":"youzhengguonei","95338":"shunfeng","950616":"jd",
}

def detect_courier(tn):
    tn = tn.strip().upper()
    for p, c in PREFIX_MAP:
        if tn.startswith(p): return c
    return None

def is_success_kd100(data):
    if data.get("status") not in ("200", 200): return False
    traces = data.get("data", [])
    if not traces: return False
    if len(traces)==1 and traces[0].get("context")=="查无结果": return False
    return True

def score_traces(traces, code):
    if not traces: return 0
    t = " ".join(tr.get("context","") for tr in traces)
    return sum(t.count(k) for k, c in TRACE_SIGNALS.items() if c==code)

def correct_courier(traces, claimed_code, api_com):
    if not traces: return claimed_code, COURIER_NAME_MAP.get(claimed_code, claimed_code)
    pc = api_com if api_com and api_com!="unknown" else claimed_code
    t = " ".join(tr.get("context","") for tr in traces)
    scores = {}
    for k, c in TRACE_SIGNALS.items():
        if k in t:
            scores[c] = scores.get(c, 0) + t.count(k)
    if scores:
        best = max(scores, key=scores.get)
        # unknown时任一信号就修正；已知代码需信号明显更强
        if best != pc and (pc in ("unknown","") or scores[best] > scores.get(pc,0)+1):
            return best, COURIER_NAME_MAP.get(best, best)
    return pc, COURIER_NAME_MAP.get(pc,pc)

def query_express(tracking_number):
    """主：聚合数据 → 备：快递100"""
    tn = tracking_number.strip()
    
    # 聚合数据
    result = query_juhe(tn)
    if result:
        update_local(tn, result["courier_code"], result["courier"], result["traces"], result["status"])
        return result
    
    # 快递100回退
    data = query_kuaidi100(tn, "auto")
    if not is_success_kd100(data):
        d = detect_courier(tn)
        if d: data = query_kuaidi100(tn, d)
    if not is_success_kd100(data) and tn.isdigit():
        best, bs = None, -1
        for c in NUMERIC_FALLBACK:
            t = query_kuaidi100(tn, c)
            if is_success_kd100(t):
                s = score_traces(t.get("data",[]), c)
                if s > bs: bs, best = s, t
        if best: data = best
    
    if not is_success_kd100(data):
        tc = data.get("data",[])
        if data.get("status") in ("200",200) and tc:
            if len(tc)==1 and tc[0].get("context")=="查无结果":
                return {"error": "单号已识别但暂无物流数据，可能尚未揽收"}
        m = data.get("message","未知错误")
        if m=="ok": return {"error": "无法识别快递公司，请确认单号"}
        return {"error": f"查询失败: {m}"}
    
    cc = data.get("com","unknown")
    cn = COURIER_NAME_MAP.get(cc, cc)
    tr = data.get("data",[])
    state = str(data.get("state","0"))
    hrd = len(tr)>0 and not (len(tr)==1 and tr[0].get("context")=="查无结果")
    traces = tr if hrd else []
    if hrd and traces:
        ncc, ncn = correct_courier(traces, cc, data.get("com",""))
        if ncc != cc: cc, cn = ncc, ncn
    
    sm = {"0":"运输中","1":"已揽收","2":"运输中","3":"已签收","4":"退签","5":"疑难","6":"退回"}
    st = "待揽收" if not hrd else sm.get(state,"运输中")
    if not hrd: traces = []
    
    update_local(tn, cc, cn, traces, st)
    return {"success":True,"tracking_number":tn,"courier":cn,"courier_code":cc,
            "status":st,"delivered":state=="3" and hrd,"traces":traces,
            "trace_count":len(traces),"has_data":hrd,"source":"kuaidi100"}

def update_local(tn, cc, cn, traces, status):
    data = load_packages()
    now = datetime.now().isoformat()
    for p in data["packages"]:
        if p["tracking_number"]==tn:
            p["courier_code"] = cc
            p["courier_name"] = cn
            p["last_status"] = status
            p["last_update"] = now
            p["delivered"] = (status=="已签收")
            if traces: p["traces"]=traces
            save_packages(data); return
    data["packages"].append({"tracking_number":tn,"courier_code":cc,"courier_name":cn,
        "label":"","added_at":now,"last_status":status,"last_update":now,
        "traces":traces,"delivered":status=="已签收"})
    save_packages(data)

def format_result(r, verbose=True):
    if "error" in r: return f"❌ {r['error']}"
    hd = r.get("has_data", r["trace_count"]>0)
    e = "✅" if r["delivered"] else ("📦" if hd else "⏳")
    lines = [f"{e} **{r['courier']}** `{r['tracking_number']}`",
             f"状态: {r['status']}{' | 共 '+str(r['trace_count'])+' 条轨迹' if hd else ''}"]
    if not hd:
        lines.append(""); lines.append("💡 快递尚未揽收，已加入追踪列表，揽收后自动更新")
    if verbose and hd and r.get("traces"):
        lines.append(""); lines.append("📋 物流轨迹:")
        for t in r["traces"]:
            lines.append(f"  {t.get('time',t.get('ftime','?'))}  {t.get('context','')}")
    if hd:
        lines.append("")
        # 高德地图路线链接
        import re as _re
        cities = []
        for t in r.get("traces",[]):
            ctx = t.get('context','')
            for m in _re.findall(r'省([一-龥a-zA-Z]{2,3})市', ctx):
                if m not in cities: cities.append(m)
        if not cities:
            for t in r.get("traces",[]):
                ctx = t.get('context','')
                for m in _re.findall(r'([一-龥a-zA-Z]{2})市', ctx):
                    if m not in cities: cities.append(m)
        if len(cities) >= 2:
            lines.append(f"🗺️ 路线: {cities[0]} → {cities[-1]} https://ditu.amap.com/dir?from={cities[0]}&to={cities[-1]}")
        elif cities:
            lines.append(f"🗺️ 位置: {cities[0]} https://www.amap.com/search?query={cities[0]}")
        else:
            lines.append(f"🗺️ 查物流: https://m.kuaidi100.com/index_all.html?type=auto&postid={r['tracking_number']}")
    return "\n".join(lines)

def save_packages(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PACKAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_packages():
    if os.path.exists(PACKAGES_FILE):
        with open(PACKAGES_FILE, "r", encoding="utf-8") as f:
            c = f.read()
            try: return json.loads(c)
            except:
                try:
                    d = json.loads(c.encode('latin-1').decode('utf-8'))
                    with open(PACKAGES_FILE,"w",encoding="utf-8") as fw:
                        json.dump(d, fw, ensure_ascii=False, indent=2)
                    return d
                except: pass
            return {"packages": []}
    return {"packages": []}

def main():
    if len(sys.argv) < 2: print("用法: python track.py <快递单号>"); sys.exit(1)
    r = query_express(sys.argv[1].strip())
    print(format_result(r))
    if "--json" in sys.argv: print("\n---JSON---\n"+json.dumps(r, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
