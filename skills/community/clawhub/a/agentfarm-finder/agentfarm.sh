#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SUBJECT="bot agent auto openclaw aiagent 8004"
ACTION="mint farm yield puzzle designed_for"
EXCLUDE="nvidia meta tesla statefarm insurance parts car vehicle ford toyota bmw mercedes rigveda -slowmist"
COUNT=30
HOURS=24

export SUBJECT ACTION EXCLUDE COUNT HOURS

log_info() { echo "[INFO] $1"; }

validate_env() {
    command -v bird &> /dev/null || { echo "bird not found"; exit 1; }
}

run() {
    validate_env
    
    cutoff_timestamp=$(($(date +%s) - HOURS*3600))
    
    log_info "=== Agentfarm-Finder ==="
    log_info "主体: $SUBJECT"
    log_info "动作: $ACTION (含固定词组 'designed for')"
    log_info "排除: $EXCLUDE + grok, nft (仅过滤时)"
    log_info "搜索: 每词 $COUNT 条"
    log_info "时间: 最近 $HOURS 小时"
    
    python3 - "$SUBJECT" "$ACTION" "$EXCLUDE" "$COUNT" "$HOURS" "$cutoff_timestamp" << 'PYTHONCODE'
import json
import subprocess
import re
from datetime import datetime
import csv
import sys

subj_str, action_str, exclude_str, count_str, hours_str, cutoff_str = sys.argv[1:]

subj_words = subj_str.split()
act_words_raw = action_str.replace('designed_for', 'designed for').split()
exclude_words = exclude_str.split()
filter_only_words = ['grok', 'nft']
COUNT = int(count_str)
HOURS = int(hours_str)
cutoff_timestamp = int(cutoff_str)

# 获取今天的日期
TODAY = datetime.now().strftime("%Y-%m-%d")

print(f"主体词: {subj_words}")
print(f"动作词: {act_words_raw}", flush=True)

seen_ids = set()
results = []

for subj in subj_words:
    for act in act_words_raw:
        if " " in act:
            query = f'"{act}" {subj} -nvidia -meta -tesla -statefarm -insurance -parts -car -vehicle -ford -toyota -bmw -mercedes -rigveda -slowmist'
        else:
            query = f"{subj} {act} -nvidia -meta -tesla -statefarm -insurance -parts -car -vehicle -ford -toyota -bmw -mercedes -rigveda -slowmist"
        
        print(f"搜索: {query}", flush=True)
        
        result = subprocess.run(["bird", "search", query, "-n", str(COUNT), "--json"], 
                                capture_output=True, text=True, timeout=30)
        raw = result.stdout
        raw = re.sub(r'[\x00-\x1F]', '', raw)
        
        if not raw or raw.strip() in ["[]", "null"]:
            continue
        
        try:
            data = json.loads(raw)
        except:
            continue
        
        for item in data:
            try:
                created_at = item.get('createdAt', '')
                if not created_at:
                    continue
                
                dt = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
                if dt.timestamp() <= cutoff_timestamp:
                    continue
                
                tweet_id = item.get('id', '')
                if tweet_id in seen_ids:
                    continue
                
                text = item.get('text', '')
                author = item.get('author', {})
                username = author.get('username', '').lower()
                name = author.get('name', '').lower()
                text_lower = text.lower()
                
                if text.startswith('@'):
                    continue
                
                if any(w in username for w in filter_only_words):
                    continue
                if any(w in name for w in filter_only_words):
                    continue
                if any(w in text_lower for w in filter_only_words):
                    continue
                
                seen_ids.add(tweet_id)
                
                results.append({
                    'id': tweet_id,
                    'text': text[:500],
                    'created_at': created_at,
                    'author': author.get('name', ''),
                    'username': author.get('username', ''),
                    'url': f"https://twitter.com/{author.get('username', '')}/status/{tweet_id}",
                    'likes': item.get('likeCount', 0),
                    'retweets': item.get('retweetCount', 0)
                })
            except Exception as e:
                continue

results.sort(key=lambda x: x['likes'] + x['retweets'], reverse=True)

output_dir = "/Users/moer/.openclaw/workspace/skills/agentfarm-finder/output"

with open(f"{output_dir}/results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False)

csv_path = f"{output_dir}/results_{TODAY}.csv"
with open(csv_path, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['热度', '作者', '用户名', '内容', '链接', '发布时间'])
    for r in results:
        writer.writerow([
            r['likes'] + r['retweets'],
            r['author'],
            r['username'],
            r['text'][:200].replace('"', '""').replace('\n', ' '),
            r['url'],
            r['created_at']
        ])

filtered_path = f"{output_dir}/results_{TODAY}_filtered.csv"
with open(csv_path, "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    filtered = [row for row in reader if int(row[0]) > 1]

with open(filtered_path, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(filtered)

print(f"=== 结果: {len(results)} 条 (过滤后 {len(filtered)} 条) ===", flush=True)

for r in results[:10]:
    print(f"[{r['likes']}❤️ {r['retweets']}🔁] @{r['username']}: {r['text'][:60]}...", flush=True)
    print(f"    🔗 {r['url']}", flush=True)

print(f"\n[TODAY] {TODAY}", flush=True)

PYTHONCODE
    
    # 用 Python 输出日期供 bash 使用
    TODAY=$(python3 -c "from datetime import datetime; print(datetime.now().strftime('%Y-%m-%d'))")
    
    log_info "JSON: ${SCRIPT_DIR}/output/results.json"
    log_info "CSV: ${SCRIPT_DIR}/output/results_${TODAY}.csv"
    log_info "过滤后: ${SCRIPT_DIR}/output/results_${TODAY}_filtered.csv"
}

run "$@"
