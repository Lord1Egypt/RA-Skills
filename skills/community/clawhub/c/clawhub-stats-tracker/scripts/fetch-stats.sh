#!/bin/bash
# ClawHub Skill 数据采集脚本
# 读取 ~/.clawhub/tracked-skills.json 中的 skill 列表，逐个调用 clawhub inspect --json 获取数据

CONFIG_FILE="${HOME}/.clawhub/tracked-skills.json"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "错误：配置文件不存在 $CONFIG_FILE"
  echo "请创建配置文件，格式参见 SKILL.md"
  exit 1
fi

# 提取所有 slug
SLUGS=$(cat "$CONFIG_FILE" | python3 -c "import sys,json; [print(s['slug']) for s in json.load(sys.stdin)['skills']]" 2>/dev/null)

if [ -z "$SLUGS" ]; then
  echo "错误：无法从配置文件中读取 skill 列表"
  exit 1
fi

# 输出表头
printf "%-30s %6s %10s %16s %16s %8s  %-18s %-18s %s\n" \
  "SLUG" "STARS" "DOWNLOADS" "CURRENT_INSTALLS" "ALLTIME_INSTALLS" "VERSION" "FIRST_PUBLISHED" "LATEST_PUBLISHED" "NOTE"
printf "%s\n" "$(printf '%.0s-' {1..160})"

# 逐个获取数据
for SLUG in $SLUGS; do
  NOTE=$(cat "$CONFIG_FILE" | python3 -c "import sys,json; skills=json.load(sys.stdin)['skills']; print(next((s['note'] for s in skills if s['slug']=='$SLUG'),''))" 2>/dev/null)

  JSON=$(npx clawhub@latest inspect "$SLUG" --json --no-input 2>/dev/null)

  if [ $? -ne 0 ] || [ -z "$JSON" ]; then
    printf "%-30s %s\n" "$SLUG" "获取失败"
    continue
  fi

  STARS=$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['skill']['stats']['stars'])" 2>/dev/null || echo "?")
  DOWNLOADS=$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['skill']['stats']['downloads'])" 2>/dev/null || echo "?")
  CURRENT=$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['skill']['stats']['installsCurrent'])" 2>/dev/null || echo "?")
  ALLTIME=$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['skill']['stats']['installsAllTime'])" 2>/dev/null || echo "?")
  VER=$(echo "$JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['latestVersion']['version'])" 2>/dev/null || echo "?")
  FIRST=$(echo "$JSON" | python3 -c "from datetime import datetime;import sys,json; print(datetime.fromtimestamp(json.load(sys.stdin)['skill']['createdAt']/1000).strftime('%Y-%m-%d %H:%M'))" 2>/dev/null || echo "?")
  LATEST=$(echo "$JSON" | python3 -c "from datetime import datetime;import sys,json; print(datetime.fromtimestamp(json.load(sys.stdin)['latestVersion']['createdAt']/1000).strftime('%Y-%m-%d %H:%M'))" 2>/dev/null || echo "?")

  printf "%-30s %6s %10s %16s %16s %8s  %-18s %-18s %s\n" \
    "$SLUG" "$STARS" "$DOWNLOADS" "$CURRENT" "$ALLTIME" "$VER" "$FIRST" "$LATEST" "$NOTE"
done
