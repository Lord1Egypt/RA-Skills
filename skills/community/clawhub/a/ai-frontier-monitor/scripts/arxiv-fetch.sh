#!/usr/bin/env bash
# arxiv-fetch.sh — 抓取 arXiv 最新 AI/ML 论文
# 用法: bash arxiv-fetch.sh [--category CAT] [--days N] [--max N] [--json]
# 默认: cs.AI+cs.LG+cs.CL, 最近7天, 最多10篇

set -e

CATEGORY="${2:-cs.AI}"
DAYS="${4:-7}"
MAX="${6:-10}"
JSON_OUT=false

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --category) CATEGORY="$2"; shift 2 ;;
    --days) DAYS="$2"; shift 2 ;;
    --max) MAX="$2"; shift 2 ;;
    --json) JSON_OUT=true; shift ;;
    *) shift ;;
  esac
done

# 计算7天前的日期
SINCE=$(date -d "-${DAYS} days" +%Y%m%d 2>/dev/null || date -v-${DAYS}d +%Y%m%d 2>/dev/null || echo "20260101")

# 构建 arXiv API 查询
# 按 category + 提交日期排序
QUERY="cat:${CATEGORY}&sortBy=submittedDate&sortOrder=descending&max_results=${MAX}"

API_URL="https://export.arxiv.org/api/query?search_query=${QUERY}"

echo "📡 正在抓取 arXiv: ${CATEGORY}（最近 ${DAYS} 天，最多 ${MAX} 篇）..." >&2

# 抓取并解析
curl -sL "$API_URL" | python3 -c "
import sys, json, re
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

xml_data = sys.stdin.read()
if not xml_data.strip():
    print(json.dumps({'error': 'empty response', 'papers': []}))
    sys.exit(0)

# arXiv Atom namespace
NS = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

try:
    root = ET.fromstring(xml_data)
except ET.ParseError:
    print(json.dumps({'error': 'parse error', 'papers': []}))
    sys.exit(0)

papers = []
for entry in root.findall('atom:entry', NS):
    title_el = entry.find('atom:title', NS)
    summary_el = entry.find('atom:summary', NS)
    published_el = entry.find('atom:published', NS)
    id_el = entry.find('atom:id', NS)
    
    if title_el is None:
        continue
    
    title = title_el.text.strip().replace('\n', ' ')
    summary = summary_el.text.strip().replace('\n', ' ')[:300] if summary_el is not None else ''
    published = published_el.text.strip()[:10] if published_el is not None else ''
    arxiv_id = id_el.text.strip().split('/')[-1] if id_el is not None else ''
    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}'
    abs_url = f'https://arxiv.org/abs/{arxiv_id}'
    
    # 作者
    authors = []
    for author in entry.findall('atom:author', NS):
        name = author.find('atom:name', NS)
        if name is not None and name.text:
            authors.append(name.text.strip())
    author_str = ', '.join(authors[:3])
    if len(authors) > 3:
        author_str += ' et al.'
    
    # 分类
    categories = []
    for cat in entry.findall('atom:category', NS):
        term = cat.get('term', '')
        if term:
            categories.append(term)
    
    papers.append({
        'title': title,
        'authors': author_str,
        'published': published,
        'arxiv_id': arxiv_id,
        'abs_url': abs_url,
        'pdf_url': pdf_url,
        'categories': categories,
        'abstract': summary
    })

# 按日期排序（最新在前）
papers.sort(key=lambda p: p['published'], reverse=True)

print(json.dumps({'papers': papers, 'count': len(papers)}, ensure_ascii=False, indent=2))
"