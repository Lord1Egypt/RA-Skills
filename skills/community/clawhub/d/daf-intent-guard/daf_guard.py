#!/usr/bin/env python3
"""DAF Intent Guard - OpenClaw skill wrapper"""
import argparse, json, math, re, sys
from datetime import datetime, timedelta

ACTION_DISTANCE = {
    ("buy","cancel"):1.0,("cancel","buy"):1.0,
    ("book","cancel"):1.0,("cancel","book"):1.0,
    ("buy","ask"):1.0,("ask","buy"):1.0,
    ("book","modify"):0.4,("modify","book"):0.4,
    ("buy","modify"):0.4,("modify","buy"):0.4,
}

def action_dist(a, b):
    if not a or not b or a==b: return 0.0
    return ACTION_DISTANCE.get((a.lower(),b.lower()), 0.8)

def parse_date(s):
    now = datetime.now().replace(hour=12,minute=0,second=0,microsecond=0)
    m = {"today":0,"tomorrow":1,"yesterday":-1,"今天":0,"明天":1,"后天":2}
    for k,d in m.items():
        if k in s: return now+timedelta(days=d)
    r = re.search(r'(\d+)\s*(天|day)',s)
    if r: return now+timedelta(days=int(r.group(1)))
    r = re.search(r'(\d+)\s*(个月|month)',s)
    if r: return now+timedelta(days=int(r.group(1))*30)
    raise ValueError(s)

def slot_dist(key, a, b):
    if a == b: return 0.0
    k = key.split("@")[0].lower()
    if any(x in k for x in ["日期","date","time","day"]):
        try:
            diff = abs((parse_date(str(a))-parse_date(str(b))).total_seconds())/3600
            return min(math.sqrt(diff/(90*24)),1.0)
        except: return 1.0
    if any(x in k for x in ["目的地","城市","destination","city","location"]):
        REGIONS = {
            "sea":["singapore","新加坡","kuala lumpur","吉隆坡","bangkok","曼谷","jakarta","胡志明市"],
            "ea": ["shanghai","上海","beijing","北京","tokyo","东京","hong kong","香港"],
            "eu": ["london","伦敦","paris","巴黎","frankfurt","amsterdam"],
            "na": ["new york","纽约","los angeles","toronto"],
        }
        def r(v):
            v=str(v).lower()
            for reg,cs in REGIONS.items():
                if any(c in v or v in c for c in cs): return reg
            return None
        r1,r2=r(a),r(b)
        if r1 and r2: return 0.3 if r1==r2 else 0.8
        return 1.0
    if any(x in k for x in ["舱位","cabin","class"]):
        lst=["economy","经济舱","premium","超经舱","business","商务舱","first","头等舱"]
        try:
            i=next(i for i,x in enumerate(lst) if str(a).lower() in x)
            j=next(j for j,x in enumerate(lst) if str(b).lower() in x)
            return abs(i-j)/max(len(lst)-1,1)
        except: return 1.0
    return 1.0

def semantic_dist(old_c, new_c, old_action=None, new_action=None):
    slots = set(old_c)|set(new_c)
    total,wsum = 0.0,0.0
    ad = action_dist(old_action, new_action)
    if ad > 0:
        wsum += ad*2.0; total += 2.0
    for s in slots:
        ov,nv = old_c.get(s),new_c.get(s)
        if ov is None or nv is None: d=0.5
        else: d=slot_dist(s,ov,nv)
        wsum+=d; total+=1.0
    return wsum/total if total>0 else 0.0

def anchor_rollback(anchors, current_idx, requires):
    req = set(requires)
    for a in anchors:
        if req & set(a.get("requires",[])):
            return max(0, current_idx-a["index"]), a["index"]
    return current_idx+1, None

def decide(sem, anc, pt=0.2, rt=0.6, pa=1, ra=2):
    if sem<=pt and anc<=pa: return "patch"
    if sem<=rt and anc<=ra: return "replan"
    return "abort"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--current-anchor", type=int, default=0)
    p.add_argument("--old-constraints", default="{}")
    p.add_argument("--new-constraints", default="{}")
    p.add_argument("--new-action", default="")
    p.add_argument("--old-action", default="")
    p.add_argument("--requires", default="[]")
    p.add_argument("--anchors", default="[]")
    p.add_argument("--patch-semantic", type=float, default=0.2)
    p.add_argument("--replan-semantic", type=float, default=0.6)
    args = p.parse_args()

    old_c = json.loads(args.old_constraints)
    new_c = json.loads(args.new_constraints)
    requires = json.loads(args.requires)
    anchors = json.loads(args.anchors)

    if args.new_action.lower() in ("cancel","abort","stop","quit"):
        print(json.dumps({"decision":"abort","reason":"cancel action","semantic_distance":1.0,"anchor_drift":0,"first_affected_anchor":None}))
        return

    anc_drift, first_affected = anchor_rollback(anchors, args.current_anchor, requires)
    if first_affected is None:
        print(json.dumps({"decision":"abort","reason":"no overlap with current task","semantic_distance":1.0,"anchor_drift":anc_drift,"first_affected_anchor":None}))
        return

    sem = semantic_dist(old_c, new_c, args.old_action, args.new_action)
    decision = decide(sem, anc_drift, args.patch_semantic, args.replan_semantic)

    print(json.dumps({
        "decision": decision,
        "semantic_distance": round(sem,3),
        "anchor_drift": anc_drift,
        "first_affected_anchor": first_affected,
        "reason": f"sem={sem:.3f} anc_drift={anc_drift}"
    }))

if __name__ == "__main__":
    main()
