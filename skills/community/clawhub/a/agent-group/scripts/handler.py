#!/usr/bin/env python3
"""极简多Agent群组处理器"""
import json, os, re
from datetime import datetime

DATA_FILE = "/root/.openclaw/workspace/memory/agent-groups.json"
AGENTS = {"搜索":{"n":"搜索","d":"擅长搜索"},"写作":{"n":"写作","d":"擅长文案"},"代码":{"n":"代码","d":"擅长编程"},"分析":{"n":"分析","d":"擅长分析"},"画图":{"n":"画图","d":"擅长绘画"}}

def load(): return json.load(open(DATA_FILE)) if os.path.exists(DATA_FILE) else {}
def save(g): os.makedirs(os.path.dirname(DATA_FILE),exist_ok=True);json.dump(g,open(DATA_FILE,'w'),ensure_ascii=False,indent=2)

def create(uid):
    g=load();g[uid]={"id":f"g{datetime.now().strftime('%Y%m%d%H%M%S')}","m":["主持人"]};save(g)
    return "✅ 群已创建！当前成员：主持人"

def add(uid,name):
    g=load()
    if uid not in g: return "❌ 先发送「建群」"
    if name in AGENTS:
        a=AGENTS[name]
        if a["n"] not in g[uid]["m"]:g[uid]["m"].append(a["n"]);save(g);return f"✅ 已邀请 @{a['n']} 进群\n📋 {a['d']}"
        return f"⚠️ @{a['n']} 已在群里"
    return f"❌ 未知的角色：{name}"

def list_(uid):
    g=load()
    if uid not in g: return "❌ 你还没有群"
    return "📋 成员：\n"+"\n".join(f"• {m}" for m in g[uid]["m"])

def dissolve(uid):
    g=load()
    if uid not in g: return "❌ 你还没有群"
    del g[uid];save(g)
    return "✅ 群已解散"

def handle(uid,text):
    t=text.strip()
    if t in ["建群","创建群"]: return create(uid)
    if t in ["退群","解散群"]: return dissolve(uid)
    if t in ["群列表","成员"]: return list_(uid)
    m=re.match(r'^(拉|邀请)(.+?)(进群|加入)$',t)
    if m: return add(uid,m.group(2).strip())
    return None

if __name__=="__main__":
    import sys
    if len(sys.argv)>=3: print(handle(sys.argv[1],sys.argv[2]))
