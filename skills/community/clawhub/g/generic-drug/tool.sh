#!/bin/bash
# generic_drug - 查询药品通用名（数据获取版）
# 脚本只负责获取 SearXNG 搜索结果并格式化，智能分析由调用者（LLM）完成

DRUG_NAME="$1"

if [ -z "$DRUG_NAME" ]; then
    echo '{"error": "请提供药品名称"}'
    exit 1
fi

# SearXNG API
SEARXNG_URL="http://localhost:8080/search"

# URL 编码查询词（将空格转换为 %20）
ENCODED_QUERY=$(echo "${DRUG_NAME} 药品通用名" | sed 's/ /%20/g')

# 调用 SearXNG 获取 JSON 结果
RESULTS_JSON=$(curl -s "${SEARXNG_URL}?q=${ENCODED_QUERY}&format=json")

# 检查是否有搜索结果
RESULT_COUNT=$(echo "$RESULTS_JSON" | jq -r '.results | length // 0')
if [ -z "$RESULT_COUNT" ] || [ "$RESULT_COUNT" = "0" ] || [ "$RESULT_COUNT" = "" ]; then
    echo "{\"drug_name\": \"${DRUG_NAME}\", \"generic_name\": \"${DRUG_NAME}\", \"found\": false, \"note\": \"无搜索结果\"}"
    exit 0
fi

# 提取前 5 个结果的标题和内容，格式化为 LLM 可读的上下文
SEARCH_CONTEXT=$(echo "$RESULTS_JSON" | jq -r '
  .results[:5] | 
  map("【\(.title)】\n\(.content // "无摘要")\n---") | 
  join("\n\n")
')

# 输出原始搜索结果和上下文，让调用者（LLM）智能分析
echo "{\"drug_name\": \"${DRUG_NAME}\", \"search_count\": ${RESULT_COUNT}, \"search_context\": \"${SEARCH_CONTEXT}\", \"note\": \"需要 LLM 分析上述搜索结果来判断通用名\"}"

# 同时输出分析提示，方便人工查看
echo ""
echo "=== 建议的 LLM 分析提示 ==="
echo "请根据以下搜索结果，判断【${DRUG_NAME}】的药品通用名：
${SEARCH_CONTEXT}

分析要求：
1. 如果找到明确的药品通用名（如"头孢克洛胶囊"的通用名是"头孢克洛"），只输出通用名本身
2. 如果该名称是辅料、基质、非药品（如"乳膏基质一号"），输出"NON_DRUG"
3. 如果找不到其他通用名，输出"ORIGINAL"（表示原名称即为通用名）
4. 不要输出任何解释，只输出一个词"
echo "=========================="
