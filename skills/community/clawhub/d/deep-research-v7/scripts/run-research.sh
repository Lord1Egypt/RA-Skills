#!/bin/bash
# 功能：执行完整深度研究流程
# 用法：bash scripts/run-research.sh <topic> [--domain <domain>] [--web]

set -e

TOPIC=$1
DOMAIN="machine learning"
ENABLE_WEB=false

# 解析参数
shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --web)
            ENABLE_WEB=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

OUTPUT_BASE="research"
TIMESTAMP=$(date +%Y-%m-%d)
OUTPUT_DIR="$OUTPUT_BASE/${TOPIC// /-}-$TIMESTAMP"

if [ -z "$TOPIC" ]; then
    echo "用法: bash scripts/run-research.sh <topic> [--domain <domain>] [--web]"
    echo "示例:"
    echo "  bash scripts/run-research.sh \"transformer efficiency\" --domain \"machine learning\""
    echo "  bash scripts/run-research.sh \"AI healthcare\" --domain healthcare --web"
    exit 1
fi

echo "=== Adaptive Depth Research v6.0 ==="
echo "主题: $TOPIC"
echo "领域: $DOMAIN"
echo "Web搜索: $([ "$ENABLE_WEB" = true ] && echo "启用" || echo "未启用")"
echo "输出: $OUTPUT_DIR"

# 创建目录结构
mkdir -p "$OUTPUT_DIR"/{sources,briefs,reports}

# ============ Step 1: 检索arXiv ============
echo ""
echo "=== Step 1: 检索 arXiv ==="
python3 << EOF
import requests
import xml.etree.ElementTree as ET
import json

topic = "$TOPIC"
url = "http://export.arxiv.org/api/query"
params = {
    'search_query': f'all:{topic}',
    'max_results': 5,
    'sortBy': 'relevance'
}

try:
    r = requests.get(url, params=params, timeout=30)
    root = ET.fromstring(r.content)
    
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        papers.append({
            'title': title[:100],
            'arxiv_id': arxiv_id,
            'pdf_url': pdf_url
        })
        print(f"  ✓ {title[:50]}...")
    
    with open('$OUTPUT_DIR/sources/arxiv_papers.json', 'w') as f:
        json.dump(papers, f, indent=2)
    
    print(f"\n找到 {len(papers)} 篇arXiv论文")
except Exception as e:
    print(f"  arXiv检索失败: {e}")
EOF

# ============ Step 2: 检索PubMed ============
echo ""
echo "=== Step 2: 检索 PubMed ==="
python3 << EOF
import requests
import json
import re

topic = "$TOPIC"
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

search_url = f"{base_url}/esearch.fcgi"
params = {'db': 'pubmed', 'term': topic, 'retmax': 5, 'sort': 'relevance', 'retmode': 'json'}

try:
    r = requests.get(search_url, params=params, timeout=15)
    ids = r.json().get('esearchresult', {}).get('idlist', [])
    
    papers = []
    for pmid in ids:
        fetch_url = f"{base_url}/efetch.fcgi"
        r2 = requests.get(fetch_url, params={'db': 'pubmed', 'id': pmid, 'retmode': 'xml'}, timeout=15)
        xml = r2.text[:10000]
        
        title_match = re.search(r'<ArticleTitle[^>]*>([^<]+)</ArticleTitle>', xml)
        title = title_match.group(1) if title_match else "N/A"
        
        papers.append({
            'title': title[:100],
            'pmid': pmid,
            'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
        })
        print(f"  ✓ {title[:50]}...")
    
    with open('$OUTPUT_DIR/sources/pubmed_papers.json', 'w') as f:
        json.dump(papers, f, indent=2)
    
    print(f"\n找到 {len(papers)} 篇PubMed论文")
except Exception as e:
    print(f"  PubMed检索失败: {e}")
EOF

# ============ Step 3: Web搜索（如启用）===========
if [ "$ENABLE_WEB" = true ]; then
    echo ""
    echo "=== Step 3: Web搜索（生成待抓取URL列表）==="
    
    # 创建待抓取URL列表
    cat > "$OUTPUT_DIR/sources/web_urls_to_fetch.txt" << URLS
# 自动生成的Web搜索URL列表
# 请手动补充相关网页URL
# 每行一个URL，#开头为注释
#
# 示例:
# https://www.mckinsey.com/industries/healthcare/...
# https://www.gartner.com/en/newsroom/...
URLS
    
    echo "⚠️  Web搜索URL列表已生成: $OUTPUT_DIR/sources/web_urls_to_fetch.txt"
    echo "   请手动补充相关URL，然后运行:"
    echo "   python3 scripts/batch-fetch.py $OUTPUT_DIR/sources/web_urls_to_fetch.txt --domain $DOMAIN"
fi

# ============ Step 4: 生成卡片 ============
echo ""
echo "=== Step 4: 生成卡片 ==="
python3 << EOF
import json
import os

output_dir = "$OUTPUT_DIR/sources"
card_num = 1

# 处理arXiv论文
try:
    with open(f'{output_dir}/arxiv_papers.json') as f:
        papers = json.load(f)
    for p in papers:
        card_id = f"card-{card_num:03d}"
        card_content = f"""---
source_id: {card_id}
source_type: arxiv
data_level: full_text_available
url: {p['pdf_url']}
---

## 来源信息
- 标题: {p['title']}
- arXiv ID: {p['arxiv_id']}
- 数据级别: 全文可获取

## 提取状态
- ⏳ 待提取: 需下载PDF并运行提取脚本
- 获取命令: python3 scripts/extract-from-pdf.py {card_id} "{p['pdf_url']}"
"""
        with open(f'{output_dir}/{card_id}.md', 'w') as f:
            f.write(card_content)
        print(f"  ✓ {card_id}: {p['title'][:40]}...")
        card_num += 1
except Exception as e:
    print(f"  arXiv卡片生成: {e}")

# 处理PubMed论文
try:
    with open(f'{output_dir}/pubmed_papers.json') as f:
        papers = json.load(f)
    for p in papers:
        card_id = f"card-{card_num:03d}"
        card_content = f"""---
source_id: {card_id}
source_type: pubmed
data_level: abstract_only
url: {p['url']}
---

## 来源信息
- 标题: {p['title']}
- PMID: {p['pmid']}
- 数据级别: 仅摘要

## 提取状态
- ⏳ 待提取: 需获取摘要或全文
- Web Fetcher: python3 scripts/fetch-card-from-web.py {card_id} "{p['url']}" --domain $DOMAIN
"""
        with open(f'{output_dir}/{card_id}.md', 'w') as f:
            f.write(card_content)
        print(f"  ✓ {card_id}: {p['title'][:40]}...")
        card_num += 1
except Exception as e:
    print(f"  PubMed卡片生成: {e}")

print(f"\n共生成 {card_num-1} 个卡片")
EOF

# ============ Step 5: 生成三层报告 ============
echo ""
echo "=== Step 5: 生成三层报告 ==="

# 执行摘要
cat > "$OUTPUT_DIR/reports/executive-summary.md" << EOF
# $TOPIC 深度研究 - 执行摘要

> 生成时间: $TIMESTAMP | 领域: $DOMAIN

## 核心结论

### ✅ 已验证结论
- [待填充] 需运行提取脚本获取具体数据

### ⚠️ 待验证结论
- [待填充] 基于摘要的线索

## 可直接行动
- [P0] 运行 \`python3 scripts/extract-from-pdf.py\` 提取arXiv论文
- [P1] 访问PubMed链接获取摘要详情
- [P1] 使用Web Fetcher抓取网页内容（如有Web源）

## Web Fetcher使用
\`\`\`bash
# 单URL抓取
python3 scripts/fetch-card-from-web.py card-web-001 "<url>" --domain $DOMAIN

# 批量抓取
python3 scripts/batch-fetch.py urls.txt --domain $DOMAIN --prefix web
\`\`\`

---

*执行摘要 - 决策者专用*
EOF

# 验证清单
cat > "$OUTPUT_DIR/reports/validation-checklist.md" << EOF
# 人工验证清单

## 数据源

| 类型 | 数量 | 获取方式 |
|------|------|----------|
| arXiv | 见sources/ | PDF提取脚本 |
| PubMed | 见sources/ | Web Fetcher抓取 |
| Web（可选）| 手动添加 | batch-fetch批量抓取 |

## 缺失指标汇总

| 优先级 | 缺失指标 | 来源卡片 | 获取路径 |
|--------|----------|----------|----------|
| P0 | 样本量 | 待提取 | 运行提取脚本 |
| P0 | AUC/准确率 | 待提取 | 运行提取脚本 |
| P1 | 成本影响 | 待提取 | Web Fetcher |

## 验证方法

### arXiv论文
\`\`\`bash
python3 scripts/extract-from-pdf.py card-xxx <pdf_url>
\`\`\`

### PubMed论文
\`\`\`bash
python3 scripts/fetch-card-from-web.py card-xxx "<pubmed_url>" --domain $DOMAIN
\`\`\`

### 网页内容
\`\`\`bash
# 单URL
python3 scripts/fetch-card-from-web.py card-web-001 "<url>" --domain $DOMAIN

# 批量
echo "<url1>" > urls.txt
echo "<url2>" >> urls.txt
python3 scripts/batch-fetch.py urls.txt --domain $DOMAIN
\`\`\`

---

*验证清单 - 执行者专用*
EOF

# 完整报告
cat > "$OUTPUT_DIR/reports/full-report.md" << EOF
# $TOPIC 深度研究报告

> **版本**: v6.0 Universal  
> **生成时间**: $TIMESTAMP  
> **领域**: $DOMAIN

---

## 方法论说明

- **检索策略**: arXiv + PubMed + Web（可选）多源检索
- **数据来源**: 见 sources/ 目录
- **提取逻辑**: 
  - arXiv/PMC: PDF全文提取
  - PubMed: Web Fetcher抓取
  - Web: Web Fetcher抓取

---

## 集成工具

### Web Fetcher
- **用途**: 抓取网页/PubMed内容
- **命令**: \`python3 scripts/fetch-card-from-web.py <card_id> <url> --domain $DOMAIN\`
- **批量**: \`python3 scripts/batch-fetch.py urls.txt --domain $DOMAIN\`

### PDF提取
- **用途**: 提取arXiv/PMC论文全文
- **命令**: \`python3 scripts/extract-from-pdf.py <card_id> <pdf_url>\`

---

## 卡片索引

[见 sources/ 目录]

---

**报告版本**: v6.0 Universal + Web Fetcher集成  
**溯源验证**: 待完成
EOF

echo "✅ 三层报告已生成"
echo "   - reports/executive-summary.md"
echo "   - reports/validation-checklist.md"
echo "   - reports/full-report.md"

# ============ 完成提示 ============
echo ""
echo "=== 研究框架已建立 ==="
echo "输出目录: $OUTPUT_DIR"
echo ""
echo "下一步:"
echo "  1. 提取arXiv论文: python3 scripts/extract-from-pdf.py card-001 <pdf_url>"
echo "  2. 抓取PubMed内容: python3 scripts/fetch-card-from-web.py card-xxx <url> --domain $DOMAIN"

if [ "$ENABLE_WEB" = true ]; then
    echo "  3. 抓取Web内容: python3 scripts/batch-fetch.py $OUTPUT_DIR/sources/web_urls_to_fetch.txt --domain $DOMAIN"
fi

echo ""
echo "Web Fetcher集成使用指南:"
echo "  - 单URL: python3 scripts/fetch-card-from-web.py <card_id> <url> --domain $DOMAIN"
echo "  - 批量:  python3 scripts/batch-fetch.py urls.txt --domain $DOMAIN --prefix web"
echo "  - 转换:  python3 scripts/convert-card-to-md.py <card_id> --by-id"
