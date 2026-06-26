#!/bin/bash

# ClawHub Top Skills Scraper
# 获取排名前20的技能

echo "========================================"
echo "  ClawHub Top 20 Skills (按总下载量)"
echo "========================================"
echo ""

clawhub explore --limit 20 --sort installsAllTime --json 2>/dev/null | jq -r '
  "排名 | 技能名称 | 总下载 | 评分 | 简介"
  "---------------------------------------------------------------------------------------------------------"
  .items[] | 
  "\(.stats.installsAllTime // 0) | \(.displayName) | \(.stats.downloads) | ⭐\(.stats.stars) | \(.summary[0:60])..."
'

echo ""
echo "========================================"
echo "  Top 20 (按近期下载)"
echo "========================================"
echo ""

clawhub explore --limit 20 --sort downloads --json 2>/dev/null | jq -r '
  "排名 | 技能名称 | 近期下载 | 总下载 | 评分"
  "-----------------------------------------------------------------------------------------------------"
  .items | 
  to_entries | 
  .[] | 
  "\(.key + 1) | \(.value.displayName) | \(.value.stats.installsCurrent) | \(.value.stats.downloads) | ⭐\(.value.stats.stars)"
'

echo ""
echo "========================================"
echo "  Top 20 (按评分)"
echo "========================================"
echo ""

clawhub explore --limit 20 --sort rating --json 2>/dev/null | jq -r '
  "排名 | 技能名称 | 评分 | 下载 | 简介"
  "-------------------------------------------------------------------------------------------------------"
  .items | 
  to_entries | 
  .[] | 
  "\(.key + 1) | \(.value.displayName) | ⭐\(.stats.stars) | \(.value.stats.downloads) | \(.summary[0:50])..."
'

echo ""
echo "========================================"
echo "  Top 20 (Trending)"
echo "========================================"
echo ""

clawhub explore --limit 20 --sort trending --json 2>/dev/null | jq -r '
  "排名 | 技能名称 | 下载 | 评分 | 简介"
  "-------------------------------------------------------------------------------------------------------"
  .items | 
  to_entries | 
  .[] | 
  "\(.key + 1) | \(.value.displayName) | \(.value.stats.downloads) | ⭐\(.value.stats.stars) | \(.summary[0:50])..."
'

echo ""
echo "✅ 完成！"
