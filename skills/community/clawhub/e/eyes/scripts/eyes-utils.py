#!/usr/bin/env python3
"""eyes-utils.py — 热点助手 (v5.0.1)
文件维护+搜索模板+分级+影响分析+格式化
命令: clean|list|dedup|templates|classify|impact|format
输入: stdin JSON 或 参数JSON; 输出: stdout JSON (format输出Markdown)
数据: ~/.openclaw/workspace/memory/eyes-sent-events.md
"""
import json, os, re, sys, time, shutil
from datetime import datetime, timezone, timedelta
CN_TZ=timezone(timedelta(hours=8))
OC=shutil.which("openclaw")or"/Users/guoxia/.npm-global/bin/openclaw"
SENT_PATH=os.path.expanduser("~/.openclaw/workspace/memory/eyes-sent-events.md")
MAX_EV=20; CLEAN_H=48

def read_events():
    if not os.path.isfile(SENT_PATH): return {"events":[],"clean_ts":None}
    with open(SENT_PATH,encoding="utf-8") as f: lines=f.readlines()
    evs,ct,pts,plv,cl=[],None,None,"",None
    for l in lines:
        m=re.search(r"清理时间:\s*(\S+\s+\S+)",l)
        if m: ct=m.group(1)
        h2=re.match(r"^## (.+)",l.strip())
        if h2:
            pts,plv,cl=None,h2.group(1),None
            m2=re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC",l)
            if m2:
                try: pts=datetime.strptime(m2.group(1),"%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc).timestamp()
                except: pass
            continue
        lv=re.match(r"^### (P[012])",l.strip())
        if lv: cl=lv.group(1); continue
        if l.strip().startswith("- ") and cl:
            evs.append({"title":l.strip()[2:].strip(),"level":cl,"push_time_utc":pts,"push_label":plv})
    return {"events":evs,"clean_ts":ct}

def write_events(events, clean_ts):
    pushes={}
    for ev in events:
        k=ev.get("push_label","未知"); pushes.setdefault(k,{"P0":[],"P1":[],"P2":[]})
        pushes[k].setdefault(ev.get("level","P2"),[]).append(ev["title"])
    lines=["# Eyes 已推送事件记录",f"# 清理时间: {clean_ts}",""]
    for pk in sorted(pushes,reverse=True):
        lines.append(f"## {pk}"); lines.append("")
        for lv in ["P0","P1","P2"]:
            for it in pushes[pk].get(lv,[]):
                lines.append(f"- {it}")
            if pushes[pk].get(lv): lines.append("")
    os.makedirs(os.path.dirname(SENT_PATH),exist_ok=True)
    with open(SENT_PATH,"w",encoding="utf-8") as f: f.write("\n".join(lines))

def read_input():
    """从stdin(管道)或argv[2](参数)读JSON, stdin优先"""
    d = ''
    if not sys.stdin.isatty():
        d = sys.stdin.read().strip()
    if not d and len(sys.argv) > 2:
        d = sys.argv[2]
    return d if d.strip() else '{"events":[]}'

def cmd_clean():
    d=read_events(); evs=d["events"]; now=time.time()
    evs=[e for e in evs if e.get("push_time_utc") is None or e["push_time_utc"]>=now-CLEAN_H*3600]
    evs.sort(key=lambda e:e.get("push_time_utc") or 0,reverse=True)
    if len(evs)>MAX_EV: evs=evs[:MAX_EV]
    ct=datetime.now(CN_TZ).strftime("%Y-%m-%d %H:%M UTC%z")
    write_events(evs,ct)
    return {"action":"clean","cleaned":len(d["events"])-len(evs),"after":len(evs),"events":evs,"clean_ts":ct}

def cmd_list():
    d=read_events()
    return {"action":"list","event_count":len(d["events"]),"events":d["events"],"clean_ts":d.get("clean_ts")}

def cmd_dedup(json_str):
    try: nd=json.loads(json_str)
    except: return {"error":"JSON解析失败","events":[]}
    ex={e["title"].lower().strip() for e in read_events()["events"]}
    uniq, dup = [], []
    for ev in nd.get("events",[]):
        t=ev.get("title","").lower().strip()
        is_dup=t in ex
        if not is_dup and len(t)>10:
            for et in ex:
                if len(t)>0 and len(et)>0 and len(set(t)&set(et))/max(len(set(t)|set(et)),1)>0.7:
                    is_dup=True; break
        (dup if is_dup else uniq).append(ev)
    return {"action":"dedup","input_count":len(nd.get("events",[])),"unique_count":len(uniq),
            "duplicate_count":len(dup),"events":uniq,"duplicates":dup}

SCENES={
    "morning":{"label":"早8点·开盘前瞻","queries":[
        {"q":"global hot topics politics economy technology latest 12 hours","l":"🌍 全球热点","p":1},
        {"q":"中国 政策 半导体 AI 新能源 股市 今日","l":"🇨🇳 国内","p":1}]},
    "hourly":{"label":"整点扫描","queries":[
        {"q":"breaking news today last hour world","l":"🌍 突发","p":1},
        {"q":"中国 突发事件 盘中 异动","l":"🇨🇳 国内","p":1}]},
    "evening":{"label":"晚8点·收盘复盘","queries":[
        {"q":"China A-share market close today sector capital flow","l":"🇨🇳 A股收盘","p":1},
        {"q":"global market overnight catalyst","l":"🌍 全球","p":1},
        {"q":"中国 政策 半导体 AI 新能源 今日重大新闻","l":"🇨🇳 产业","p":2}]},
}
def cmd_templates(scene=""):
    # 自动根据北京时间推断scene，避免模型在UTC环境下误判时段
    now_bj = datetime.now(CN_TZ)
    h = now_bj.hour
    if h == 8:
        inferred = "morning"
    elif 9 <= h < 20:
        inferred = "hourly"
    else:
        inferred = "evening"
    # 始终根据北京时间自动推断scene，忽略模型传入的值
    return SCENES[inferred]

P0_KW=["战争","战事","开火","入侵","导弹","袭击","熔断","崩盘","crash","earthquake",
       "核","nuclear","加息","降息","美联储","FOMC","非农","NFP","CPI","PPI","sanction"]
P1_KW=["政策","发布","关税","tariff","突破","breakthrough","涨停","跌停","北向","万亿",
       "收购","并购","产能","降准","利率","财报","业绩","异动"]
def cmd_classify(json_str):
    try: nd=json.loads(json_str)
    except: return {"error":"JSON解析失败","events":[]}
    res=[]
    for ev in nd.get("events",[]):
        t=ev.get("title","").lower()
        p0=sum(1 for k in P0_KW if k.lower() in t)
        p1=sum(1 for k in P1_KW if k.lower() in t)
        lv="P0" if p0>=1 else "P1" if p1>=1 else "P2"
        cf=min(0.5+p0*0.15,0.95) if p0 else min(0.5+p1*0.1,0.85) if p1 else 0.5
        res.append({"title":ev.get("title",""),"level":lv,"confidence":round(cf,2),
                    "p0_hits":p0,"p1_hits":p1})
    return {"action":"classify","input_count":len(nd.get("events",[])),"events":res}

IMPACT_RULES=[
    ("战争/冲突",["战争","冲突","导弹","入侵","袭击","军事","开火"],
     ["原油↑→航运↑→军工↑→黄金↑","天然气↑→粮食↑→军工↑","全球避险↑"],
     ["中远海控","中船防务","山东黄金","军工ETF"]),
    ("地缘/贸易",["关税","制裁","贸易战","脱钩","出口管制"],
     ["国产替代↑→半导体","自主可控↑→信创"],
     ["中芯国际","北方华创","中科曙光","海光信息"]),
    ("重大政策",["降息","加息","利率","政策","监管","央行","美联储"],
     ["美元→新兴市场→北向","流动性↑→银行地产↑","行业波动"],
     ["招商银行","万科A","保利发展","浪潮信息"]),
    ("创新技术",["AI","人工智能","芯片","半导体","量子","固态","无人","低空"],
     ["算力↑→芯片↑→AI应用","新能源车→锂电","军工智能化"],
     ["寒武纪","科大讯飞","海光信息","中微公司","宁德时代"]),
    ("经济数据",["GDP","PMI","CPI","PPI","社融","非农","失业","通胀"],
     ["利率预期→美元/美债→股市","经济预期→A股方向"],
     ["沪深300ETF","消费ETF","周期ETF"]),
    ("金融市场",["熔断","涨停","跌停","北向","万亿","异动","轮动"],
     ["情绪传导→板块轮动","外资动向→核心资产","券商受益/承压"],
     ["东方财富","中信证券","同花顺"]),
    ("商品/汇率",["原油","天然气","黄金","汇率","人民币","比特币","铜","铝","锂"],
     ["能源→化工→通胀","避险→采矿股","出口/进口影响"],
     ["中国石油","万华化学","紫金矿业","山东黄金"]),
]
def cmd_impact(json_str):
    try: nd=json.loads(json_str)
    except: return {"error":"JSON解析失败","events":[]}
    res=[]
    for ev in nd.get("events",[]):
        t=ev.get("title","").lower(); cats,chs,stks=[],[],[]
        for cat,kws,ch_ls,stk_ls in IMPACT_RULES:
            if any(k.lower() in t for k in kws):
                cats.append(cat); chs.extend(ch_ls); stks.extend(stk_ls)
        res.append({"title":ev.get("title",""),"level":ev.get("level","P2"),
                    "matched_categories":cats,"impact_chains":chs[:3],
                    "related_stocks":sorted(set(stks))[:8]})
    return {"action":"impact","input_count":len(nd.get("events",[])),"events":res}

def cmd_format(scene, json_str, manual=False):
    try: nd=json.loads(json_str) if json_str else {}
    except: nd={}
    now_bj = datetime.now(CN_TZ)
    h = now_bj.hour
    # 根据实际北京时间确定标题和内容格式，忽略传入的scene
    if h == 8:
        inferred_scene = "morning"
        label = "☀️ 早8点"
    elif 9 <= h < 20:
        inferred_scene = "hourly"
        label = "⏰ 整点扫描"
    else:
        inferred_scene = "evening"
        label = "晚8点"
    if manual:
        lines=["👁️ **Eyes · 大眼看世界**",""]
    else:
        if inferred_scene == "morning":
            lines=[f"👁️ **Eyes · 大眼看世界** ☀️ 早8点",""]
        elif inferred_scene == "hourly":
            lines=[f"👁️ **Eyes · 大眼看世界** ⏰ 整点扫描",""]
        else:
            lines=[f"👁️ **Eyes · 大眼看世界** 🌙 {label}",""]
    lines.append("**📊 今日要闻**")
    for ev in nd.get("events",[]):
        icon={"P0":"🔴","P1":"🟡","P2":"🟢"}.get(ev.get("level","P2"),"🟢")
        lines.append(f"**{icon} {ev.get('level','P2')} {ev.get('title','')}**")
        if ev.get("impact_chains"): lines.append(f"  → 影响: {' | '.join(ev['impact_chains'])}")
        if ev.get("related_stocks"): lines.append(f"  → 相关: {'/'.join(ev['related_stocks'][:5])}")
        lines.append("")  # 事件间空行,供分段
    if inferred_scene in ("morning","evening"):
        as_=nd.get("a_share",{}); lines.append("**📈 市场分析**")
        if as_.get("summary"): lines.append(f"  {as_['summary']}")
        if as_.get("sectors"): lines.append(f"  → 板块: {' | '.join(as_['sectors'][:5])}")
        lines.append("")
    if inferred_scene=="evening":
        lines.append("**🔮 明日关注**")
        lines.append(f"  {nd.get('tomorrow','(待模型补充)')}" if nd.get('tomorrow') else "  (待模型补充)")
        lines.append("")
    lines.append("💬 想关注什么方向的股票？")
    return "\n".join(lines)

def segment_text(text, max_chars=500):
    blocks=text.split("\n\n"); segs,cur=[],""
    for blk in blocks:
        blk=blk.strip()
        if not blk: continue
        if cur and len(cur)+len(blk)+2>max_chars:
            segs.append(cur.strip()); cur=blk
        else: cur=(cur+"\n\n"+blk) if cur else blk
    if cur: segs.append(cur.strip())
    if segs and len(segs[0])<100 and len(segs)>1:
        segs[1]=segs[0]+"\n\n"+segs[1]; segs.pop(0)
    if len(segs)<=1 and cur and len(cur)>max_chars:
        lines=cur.split("\n"); segs,cur=[],""
        for ln in lines:
            if cur and len(cur)+len(ln)+1>max_chars:
                segs.append(cur.strip()); cur=ln
            else: cur=(cur+"\n"+ln) if cur else ln
        if cur: segs.append(cur.strip())
    return segs

def cmd_send_segments(json_str=None):
    """读取含---SEGMENT---标记的文本，自动逐段发送到飞书。
    json_str: 直接传入JSON字符串（推荐），否则从stdin读。
    输入JSON: {"content": "含标记完整文本", "channel": "feishu", "target": "ou_xxx"}
    """
    import subprocess, time
    openclaw_bin = OC
    if json_str is None:
        json_str = sys.argv[2] if len(sys.argv) > 2 else ''
        # 如果argv也没有，尝试从stdin读（支持管道：format | send-segments）
        if not json_str and not sys.stdin.isatty():
            json_str = sys.stdin.read().strip()
    try: nd=json.loads(json_str) if json_str else {}
    except: return {"error":"JSON解析失败"}
    content=nd.get("content","")
    channel=nd.get("channel")
    target=nd.get("target","")
    # 若channel/target未提供则从bigA共享配置读取
    if not channel or not target:
        try:
            with open(os.path.expanduser('~/.openclaw/workspace/memory/biga-send-config.json')) as f:
                cfg=json.load(f)
            if not channel: channel=cfg.get('channel')
            if not target: target=cfg.get('target')
        except: pass
    if not content or not target or not channel:
        return {"error":"缺少发送参数(content/channel/target)"}
    # 自动检测安装状态，在内容上追加/前置提示（不依赖模型判断）
    wrk = os.path.expanduser('~/.openclaw/workspace/memory')
    if not os.path.exists(wrk + '/eyes-installed'):
        content = '⚠️ Eyes 定时器未配置，回复「帮我安装」设置每日热点推送\n\n' + content
    if not os.path.exists(wrk + '/biga-installed'):
        content += '\n\n💡 还没装 BigA（智能选股工具），回复「帮我安装大A」试试？'
    parts=content.split("---SEGMENT---")
    segs=[p.strip() for p in parts if p.strip()]
    # 自动分段：若---SEGMENT---切分只得到1段且内容>500字，按双换行自动切分
    if len(segs) <= 1 and len(content) > 500:
        from re import split as re_split
        auto_parts=re_split(r'\n{2,}', content)
        # 只保留>50字的段落，避免切出太碎
        auto_segs=[]
        for p in auto_parts:
            p=p.strip()
            if not p: continue
            if auto_segs and len(p) < 50:
                auto_segs[-1] += '\n\n' + p
            else:
                auto_segs.append(p)
        if len(auto_segs) > 1:
            segs=auto_segs
    # 合并小段：低于250字的段并入前一段（合并后不超过600字，避免超飞书限制）
    merged=[]
    for seg in segs:
        if merged and len(seg) < 250:
            combined = merged[-1] + "\n\n" + seg
            if len(combined) <= 600:
                merged[-1] = combined
            else:
                merged.append(seg)
        else:
            merged.append(seg)
    segs=merged
    results=[]
    for i,seg in enumerate(segs):
        seg=seg.strip()
        if not seg: continue
        for attempt in range(3):
            p=subprocess.Popen(
                [openclaw_bin,"message","send",
                 "--channel",channel,
                 "--target",target,
                 "--message",seg,
                 "--json"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            stdout,stderr=p.communicate(timeout=15)
            ok=False
            if p.returncode==0:
                try:
                    resp=json.loads(stdout.decode())
                    ok=resp.get("payload",{}).get("ok",False)
                except:
                    ok=False
            if ok:
                results.append({"segment":i+1,"status":"sent","attempt":attempt+1})
                break
            time.sleep(1)
        else:
            results.append({"segment":i+1,"status":"failed","attempt":3})
    sent=sum(1 for r in results if r["status"]=="sent")
    return {"action":"send-segments","total":len(segs),"sent":sent,
            "failed":len(segs)-sent,"details":results}

def main():
    if len(sys.argv)<2: print(__doc__,file=sys.stderr); sys.exit(1)
    cmd=sys.argv[1]
    if cmd=="clean": print(json.dumps(cmd_clean(),ensure_ascii=False))
    elif cmd=="list": print(json.dumps(cmd_list(),ensure_ascii=False))
    elif cmd=="dedup": print(json.dumps(cmd_dedup(read_input()),ensure_ascii=False))
    elif cmd=="templates":
        sc=""
        for i,a in enumerate(sys.argv):
            if a=="--scene" and i+1<len(sys.argv): sc=sys.argv[i+1]
        print(json.dumps(cmd_templates(sc),ensure_ascii=False))
    elif cmd=="classify": print(json.dumps(cmd_classify(read_input()),ensure_ascii=False))
    elif cmd=="impact": print(json.dumps(cmd_impact(read_input()),ensure_ascii=False))
    elif cmd=="format":
        sc,seg,manual="evening",False,False
        for i,a in enumerate(sys.argv):
            if a=="--scene" and i+1<len(sys.argv): sc=sys.argv[i+1]
            if a in ("--segments","-s"): seg=True
            if a in ("--manual","-m"): manual=True
        if sc not in ("morning","hourly","evening"): sc="evening"
        text=cmd_format(sc,read_input(),manual=manual)
        if seg:
            print("\n---SEGMENT---\n".join(segment_text(text)))
        else:
            print(text)
    elif cmd=="send-segments":
        json_arg = ''
        file_path = ''
        for i,a in enumerate(sys.argv):
            if a=="--file" and i+1<len(sys.argv): file_path=sys.argv[i+1]
        if file_path:
            try:
                with open(file_path) as f:
                    lines=f.readlines()
                    # 跳过可能的shebang和空行
                    content=''.join(l for l in lines if not l.startswith('#!'))
                import json as _j
                json_arg = _j.dumps({'content': content}, ensure_ascii=False)
            except Exception as e:
                print(json.dumps({'error': f'读取文件失败: {e}'}, ensure_ascii=False))
                return
        else:
            json_arg = sys.argv[2] if len(sys.argv) > 2 else ''
        result = cmd_send_segments(json_arg)
        print(json.dumps(result, ensure_ascii=False))
    else: print(f"未知命令: {cmd}",file=sys.stderr); sys.exit(1)

if __name__=="__main__": main()
