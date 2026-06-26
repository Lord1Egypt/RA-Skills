#!/bin/bash
# 功能：执行完整深度研究流程
# 用法：bash scripts/run-research.sh <topic> [--domain <domain>]

set -e

TOPIC=$1
DOMAIN=${2:-"machine learning"}
OUTPUT_BASE="research"
TIMESTAMP=$(date +%Y-%m-%d)
OUTPUT_DIR="$OUTPUT_BASE/${TOPIC// /-}-$TIMESTAMP"

if [ -z "$TOPIC" ]; then
    echo "用法: bash scripts/run-research.sh <topic> [--domain <domain>]"
    echo "示例: bash scripts/run-research.sh \"transformer efficiency\" --domain \"machine learning\""
    exit 1
fi

echo "=== Adaptive Depth Research v6.0 ==="
echo "主题: $TOPIC"
echo "领域: $DOMAIN"
echo "输出: $OUTPUT_DIR"

# 创建目录结构
mkdir -p "$OUTPUT_DIR"/{sources,briefs,reports}

# Step 1: 检索arXiv
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

# Step 2: 检索PubMed
echo ""
echo "=== Step 2: 检索 PubMed ==="
python3 << EOF
import requests
import json
import re

topic = "$TOPIC"
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# 搜索
search_url = f"{base_url}/esearch.fcgi"
params = {'db': 'pubmed', 'term': topic, 'retmax': 5, 'sort': 'relevance', 'retmode': 'json'}

try:
    r = requests.get(search_url, params=params, timeout=15)
    ids = r.json().get('esearchresult', {}).get('idlist', [])
    
    papers = []
    for pmid in ids:
        # 获取摘要
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

# Step 3: 生成卡片
echo ""
echo "=== Step 3: 生成卡片 ==="
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
except:
    pass

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
- 获取命令: 访问 {p['url']}
"""
        with open(f'{output_dir}/{card_id}.md', 'w') as f:
            f.write(card_content)
        print(f"  ✓ {card_id}: {p['title'][:40]}...")
        card_num += 1
except:
    pass

print(f"\n共生成 {card_num-1} 个卡片")
EOF

# Step 4: 生成三层报告
echo ""
echo "=== Step 4: 生成三层报告 ==="

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

---

*执行摘要 - 决策者专用*
EOF

# 验证清单
cat > "$OUTPUT_DIR/reports/validation-checklist.md" << EOF
# 人工验证清单

## 缺失指标汇总

| 优先级 | 缺失指标 | 来源卡片 | 获取路径 |
|--------|----------|----------|----------|
| P0 | 样本量 | card-001 | 运行提取脚本 |
| P0 | AUC/准确率 | card-001 | 运行提取脚本 |
| P1 | 成本影响 | card-002 | 访问PubMed |

## 验证方法

### arXiv论文
1. 运行 \`python3 scripts/extract-from-pdf.py card-xxx <pdf_url>\`
2. 检查提取结果中的关键指标

### PubMed论文
1. 访问PubMed链接
2. 点击 "Full Text" 尝试获取全文
3. 如付费，查看摘要或联系作者

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

- **检索策略**: arXiv + PubMed 多源检索
- **数据来源**: 见 sources/ 目录
- **提取逻辑**: 通用 Prompt + 领域配置

---

## 已验证结论

[待填充: 运行提取脚本后更新]

---

## 待验证线索

[待填充: 基于摘要的线索]

---

## 战略建议

### 短期
- 运行提取脚本获取arXiv论文数据

### 中期
- 访问PubMed获取摘要详情

### 长期
- 补充更多数据源

---

## 附录: 卡片索引

[见 sources/ 目录]

---

**报告版本**: v6.0 Universal  
**溯源验证**: 待完成
EOF

echo "✅ 三层报告已生成"
echo "   - reports/executive-summary.md"
echo "   - reports/validation-checklist.md"
echo "   - reports/full-report.md"

echo ""
echo "=== 研究完成 ==="
echo "下一步: 运行提取脚本获取具体数据"
echo "  python3 scripts/extract-from-pdf.py card-001 <pdf_url>"