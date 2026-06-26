#!/bin/bash
# arXiv 每日论文精选 - 执行脚本

set -e

# 搜索关键词（LLM/RAG/Agent 相关）
SEARCH_QUERIES=(
  "cat:cs.AI+AND+all:large+language+model"
  "cat:cs.CL+AND+all:retrieval+augmented+generation"
  "cat:cs.AI+AND+all:agent"
  "cat:cs.LG+AND+all:transformer"
  "cat:cs.AI+AND+all:reasoning"
)

# 获取论文数据
fetch_papers() {
  local query="$1"
  local max_results="${2:-5}"
  
  curl -s "http://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=${max_results}" \
    | xmllint --noent - 2>/dev/null \
    || curl -s "http://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=${max_results}"
}

# 解析 XML 提取论文信息（简化版）
parse_entry() {
  local xml="$1"
  echo "$xml" | grep -oP '(?<=<title>)[^<]+' | head -1
}

echo "🔍 开始搜集 arXiv 最新论文..."
echo ""

# 获取论文
for query in "${SEARCH_QUERIES[@]}"; do
  echo "搜索：$query"
  fetch_papers "$query" 3
  echo "---"
done

echo ""
echo "✅ 搜集完成"
