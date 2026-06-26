#!/bin/bash
# 功能：根据数据源自动选择全文/摘要模式，调用通用提取Prompt
# 用法：bash scripts/fetch-and-extract.sh <source_url>

set -e

SOURCE_URL=$1
CONFIG_FILE="config/research-config.yaml"
OUTPUT_DIR="sources"

if [ -z "$SOURCE_URL" ]; then
    echo "用法: bash scripts/fetch-and-extract.sh <source_url>"
    exit 1
fi

# 1. 判断数据源类型
if echo "$SOURCE_URL" | grep -q "arxiv.org"; then
    SOURCE_TYPE="arxiv"
    HAS_FULL_TEXT=true
    # 转换arXiv URL为PDF URL
    PDF_URL=$(echo "$SOURCE_URL" | sed 's|/abs/|/pdf/|')
    
elif echo "$SOURCE_URL" | grep -q "ncbi.nlm.nih.gov/pmc"; then
    SOURCE_TYPE="pubmed_central"
    HAS_FULL_TEXT=true
    PDF_URL="$SOURCE_URL/pdf"
    
elif echo "$SOURCE_URL" | grep -q "pubmed.ncbi.nlm.nih.gov"; then
    SOURCE_TYPE="pubmed_abstract"
    HAS_FULL_TEXT=false
    
elif echo "$SOURCE_URL" | grep -q "doi.org"; then
    SOURCE_TYPE="doi"
    HAS_FULL_TEXT=false
    
else
    SOURCE_TYPE="web"
    HAS_FULL_TEXT=false
fi

echo "=== 数据源类型: $SOURCE_TYPE ==="
echo "全文可用: $HAS_FULL_TEXT"

# 2. 生成卡片ID
CARD_ID="card-$(date +%s | md5sum | head -c 8)"
CARD_FILE="$OUTPUT_DIR/${CARD_ID}.md"

mkdir -p "$OUTPUT_DIR"

# 3. 获取文本内容
if [ "$HAS_FULL_TEXT" = true ] && [ -n "$PDF_URL" ]; then
    echo "下载PDF: $PDF_URL"
    
    # 使用python脚本提取
    python3 scripts/extract-from-pdf.py "$CARD_ID" "$PDF_URL" 2>/dev/null || {
        echo "PDF提取失败，尝试摘要模式"
        HAS_FULL_TEXT=false
    }
    
    if [ "$HAS_FULL_TEXT" = true ]; then
        # 读取提取结果
        EXTRACTED_JSON="/tmp/${CARD_ID}_extracted.json"
        if [ -f "$EXTRACTED_JSON" ]; then
            TEXT_TYPE="full_text"
            DATA_LEVEL="full_text"
        else
            HAS_FULL_TEXT=false
        fi
    fi
fi

if [ "$HAS_FULL_TEXT" = false ]; then
    echo "使用摘要模式..."
    TEXT_TYPE="abstract"
    DATA_LEVEL="abstract_only"
    
    # 对于PubMed，获取摘要
    if [ "$SOURCE_TYPE" = "pubmed_abstract" ]; then
        PMID=$(echo "$SOURCE_URL" | grep -oP '\d+')
        python3 << EOF
import requests
import json
import re

pmid = "$PMID"
url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
r = requests.get(url, timeout=30)
xml = r.text[:15000]

# 提取标题
title = re.search(r'<ArticleTitle[^>]*>([^<]+)</ArticleTitle>', xml)
title = title.group(1) if title else "N/A"

# 提取摘要
abstracts = re.findall(r'<AbstractText[^>]*>([^<]+)</AbstractText>', xml)
abstract = ' '.join(abstracts)[:800]

# 提取样本量
sample = None
sample_match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*(?:patients|subjects|participants)', abstract, re.I)
if sample_match:
    sample = sample_match.group(1)

result = {
    "title": title,
    "abstract": abstract,
    "sample_size": sample,
    "pmid": pmid
}

with open("/tmp/${CARD_ID}_abstract.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"标题: {title[:50]}...")
if sample:
    print(f"样本量: {sample}")
EOF
        EXTRACTED_JSON="/tmp/${CARD_ID}_abstract.json"
    fi
fi

# 4. 生成卡片
echo "生成卡片: $CARD_FILE"

cat > "$CARD_FILE" << EOF
---
source_id: $CARD_ID
source_type: $SOURCE_TYPE
data_level: $DATA_LEVEL
url: $SOURCE_URL
retrieved_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

## 来源信息
- 类型: $SOURCE_TYPE
- 数据级别: $DATA_LEVEL
- URL: $SOURCE_URL

## 提取结果
$(if [ -f "$EXTRACTED_JSON" ]; then cat "$EXTRACTED_JSON"; else echo "提取待完成"; fi)

## 验证状态
- $(if [ "$DATA_LEVEL" = "full_text" ]; then echo "✅ 全文已提取"; else echo "⚠️ 仅摘要，需验证"; fi)
- 缺失指标: 待补充
- 验证路径: 访问原文 $SOURCE_URL
EOF

echo "✅ 卡片已生成: $CARD_FILE"
echo "   数据级别: $DATA_LEVEL"