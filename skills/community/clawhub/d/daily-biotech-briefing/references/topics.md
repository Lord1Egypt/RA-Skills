# WeChat Search Topics (curl-based, anti-spider bypass)

Search each topic using the curl-based search script. **DO NOT use `node search_wechat.js`** — it's blocked by Sogou's TLS fingerprint detection.

```bash
cd ~/.openclaw/workspace/skills/wechat-article-search/scripts

# Topic 1: 干细胞治疗
./search_wechat_curl.sh "干细胞 治疗" -n 50 -o /tmp/wx_stemcell.json

# WAIT 3-5s between searches to avoid IP-rate limiting
sleep 5 && ./search_wechat_curl.sh "外泌体 治疗" -n 50 -o /tmp/wx_exosome.json

# Topic 3: 质谱诊断 — 多关键词轮换
sleep 5 && ./search_wechat_curl.sh "临床质谱" -n 30 -o /tmp/wx_ms_1.json
sleep 5 && ./search_wechat_curl.sh "质谱 临床 检测" -n 20 -o /tmp/wx_ms_2.json

# Topic 4: 拉曼诊断 — 多关键词轮换
sleep 5 && ./search_wechat_curl.sh "拉曼 临床 检测" -n 20 -o /tmp/wx_raman_1.json
sleep 5 && ./search_wechat_curl.sh "SERS 检测 临床" -n 20 -o /tmp/wx_raman_2.json
sleep 5 && ./search_wechat_curl.sh "表面增强拉曼 检测" -n 10 -o /tmp/wx_raman_3.json

# Topic 5: 卵巢癌检测
sleep 5 && ./search_wechat_curl.sh "卵巢癌 检测" -n 50 -o /tmp/wx_ovarian.json
```

## Merge multi-keyword results

For topics 3 and 4 (multi-keyword), merge after searching:

```python
import json

# Topic 3 merge: 质谱
all_articles = []
seen = set()
for f in ['/tmp/wx_ms_1.json', '/tmp/wx_ms_2.json']:
    try:
        d = json.load(open(f))
        for a in d.get('articles', []):
            if a['title'] not in seen:
                seen.add(a['title'])
                all_articles.append(a)
    except: pass
json.dump({'articles': all_articles[:50]}, open('/tmp/wx_ms.json', 'w'), ensure_ascii=False)

# Topic 4 merge: 拉曼
all_articles = []
seen = set()
for f in ['/tmp/wx_raman_1.json', '/tmp/wx_raman_2.json', '/tmp/wx_raman_3.json']:
    try:
        d = json.load(open(f))
        for a in d.get('articles', []):
            if a['title'] not in seen:
                seen.add(a['title'])
                all_articles.append(a)
    except: pass
json.dump({'articles': all_articles[:50]}, open('/tmp/wx_raman.json', 'w'), ensure_ascii=False)
```

## ⚠️ Sogou redirect links — DO NOT try to resolve them

The search returns sogou redirect links like `https://weixin.sogou.com/link?url=...`. These CANNOT be resolved to mp.weixin.qq.com URLs (triggers anti-spider). Use the search summaries as-is — they are detailed enough for briefing purposes.

## Time Filter (48 hours)

Same as before — run Python time filter on each merged JSON. The `datetime` field is in `YYYY-MM-DD HH:MM:SS` format (Asia/Shanghai timezone).
