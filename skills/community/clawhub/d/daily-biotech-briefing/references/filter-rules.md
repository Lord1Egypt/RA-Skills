# Article Filter Rules

After time-filtering (48h), apply these rules to remove 科普/标题党 articles.

## 🚫 REJECT — Title Pattern

Articles whose title matches these patterns should be discarded:

1. **Sensationalist / Clickbait**:
   - Contains phrases like: "震惊", "不为人知", "你绝对想不到", "太神奇了"
   - Excessive exclamation marks (2+ "！" or "!")
   - ALL CAPS or excessive emoji in title

2. **Health/Beauty MLM style**:
   - "让XXX年轻", "逆龄", "冻龄", "返老还童"
   - "美容", "抗衰" in overly commercial tone
   - "天然", "神奇", "秘方" combined with disease claims

3. **Popular Science without substance**:
   - Title starts with "什么是", "一文读懂", "科普", "带你了解" followed by basics
   - Pure definitions/introductions without new research or clinical data

4. **Marketing/Advertising**:
   - Contains "点击购买", "限时优惠", "免费领取"
   - Company/product promotion without research content

5. **Stale / Republished old content**:
   - Summary or title indicates republishing of old research
   - "回顾", "盘点" of past years (unless it's a 2026 annual review)

## ✅ ACCEPT — Keep these

Articles that demonstrate genuine research/regulatory value:

1. **Clinical research**: Contains actual clinical data, patient outcomes, trial phases
2. **Regulatory updates**: NMPA/CDE decisions, new guidelines, expert consensus
3. **Technology breakthroughs**: Novel methods, instrument advances, new biomarkers
4. **Published research**: References to journal publications (DOI, journal name)
5. **Industry policy**: Government policy changes affecting the field

## Post-Filter Limit

After filtering, keep top 3-5 articles per topic by relevance/date. **If all are filtered out, mark the topic as empty — never supplement with non-WeChat content.**

## Python Filter Implementation

```python
import json, datetime, re

REJECT_PATTERNS = [
    r'震惊', r'不为人知', r'你绝对想不到', r'太神奇了',
    r'！！', r'!!',
    r'让.*年轻', r'逆龄', r'冻龄', r'返老还童',
    r'天然秘方', r'神奇秘方',
    r'点击购买', r'限时优惠', r'免费领取',
    r'^什么是', r'^一文读懂', r'^科普', r'^带你了解',
]

ACCEPT_PATTERNS = [
    r'临床', r'试验', r'患者', r'疗效',
    r'NMPA', r'CDE', r'FDA', r'批准', r'指南', r'共识',
    r'突破', r'新方法', r'新技术', r'标志物',
    r'DOI', r'发表', r'期刊',
    r'政策', r'产业', r'监管',
]

with open('/tmp/wx_<topic>.json') as f:
    data = json.load(f)

filtered = []
for a in data['articles']:
    title = a.get('title', '')
    summary = a.get('summary', '')
    text = title + ' ' + summary
    
    # Reject check
    if any(re.search(p, text) for p in REJECT_PATTERNS):
        continue
    
    # Accept check
    if any(re.search(p, text) for p in ACCEPT_PATTERNS):
        filtered.append(a)

# Sort by datetime descending, keep top 5
filtered.sort(key=lambda x: x.get('datetime', ''), reverse=True)
filtered = filtered[:5]

print(f"After content filter: {len(filtered)} articles")
for a in filtered:
    print(f"  - {a['title']} ({a.get('datetime', '?')})")
```
