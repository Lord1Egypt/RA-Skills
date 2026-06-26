#!/usr/bin/env python3
import json, os
from datetime import datetime, timezone

IN_FILE = '/root/.openclaw/workspace/data/harvest/feature_patterns.json'
OUT_JSON = '/root/.openclaw/workspace/data/harvest/opportunities.json'
OUT_MD = '/root/.openclaw/workspace/data/harvest/opportunities.md'
os.makedirs('/root/.openclaw/workspace/data/harvest', exist_ok=True)

def impact_from_text(t):
    t=t.lower()
    if any(k in t for k in ['agent','copilot','workflow','automation']): return 5
    if any(k in t for k in ['sdk','api','studio','model']): return 4
    return 3

def effort_from_text(t):
    t=t.lower()
    if any(k in t for k in ['platform','studio']): return 4
    if any(k in t for k in ['agent','workflow','copilot']): return 3
    return 2

with open(IN_FILE,'r',encoding='utf-8') as f:
    items = json.load(f).get('items',[])

ops=[]
for p in items[:20]:
    title=p.get('name','')
    impact=impact_from_text(title)
    effort=effort_from_text(title)
    score=impact*2-effort
    o={
      'title': title,
      'type': 'skill' if 'agent' in title.lower() or 'workflow' in title.lower() else 'app',
      'priority': p.get('priority','P1'),
      'impact': impact,
      'effort': effort,
      'score': score,
      'why_now': p.get('coreValue','市场窗口期出现，且可快速验证'),
      'mvp_steps': [
        '定义输入输出协议',
        '实现最小可运行脚本',
        '接入可视化状态页',
        '进行一轮真实数据验证'
      ]
    }
    ops.append(o)

ops.sort(key=lambda x:(x['priority'], -x['score']))
payload={'generatedAt': datetime.now(timezone.utc).isoformat(), 'count':len(ops), 'items':ops}
with open(OUT_JSON,'w',encoding='utf-8') as f:
    json.dump(payload,f,ensure_ascii=False,indent=2)

lines=['# Build Opportunities\n']
for i,o in enumerate(ops[:12],1):
    lines.append(f"## {i}. {o['title']} ({o['type']})")
    lines.append(f"- Priority: {o['priority']} | Impact: {o['impact']} | Effort: {o['effort']} | Score: {o['score']}")
    lines.append(f"- Why now: {o['why_now']}")
    lines.append('- MVP: ' + ' -> '.join(o['mvp_steps']))
    lines.append('')
with open(OUT_MD,'w',encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('generated', OUT_JSON, len(ops))
print('generated', OUT_MD)
