---
name: cnki-scholar
description: "中文学术论文搜索工具。搜索中英文论文，覆盖知网、万方、维普等中文数据库的论文。Use when: 用户说「搜论文」「查文献」「知网」「CNKI」「搜索中文学术论文」「找中文文献」，或需要搜索、下载、引用中英文论文。支持OpenAlex API（免费，2亿+论文）和Crossref API（DOI覆盖）。Also activate when: 用户需要学术搜索、论文元数据提取、引用格式生成。"
---

# CNKI Scholar — 中文学术论文搜索

基于OpenAlex和Crossref API的学术搜索工具，覆盖中英文论文（包括知网收录的论文）。

## 数据源

| 数据源 | 覆盖范围 | 优势 | 限制 |
|--------|----------|------|------|
| **OpenAlex** | 2亿+论文 | 免费、数据全、有被引量 | 部分中文论文元数据不完整 |
| **Crossref** | DOI论文 | DOI解析准确 | 无被引量、中文覆盖少 |
| **百度学术** | 中英文 | 知网论文覆盖好 | 需浏览器自动化 |

## 核心功能

### 1. 搜索论文

使用OpenAlex API搜索：

```bash
curl -s "https://api.openalex.org/works?search=YOUR_QUERY&per_page=10"
```

支持的筛选参数：
- `search=` — 关键词搜索
- `filter=publication_year:2020-2025` — 年份范围
- `filter=cited_by_count:>10` — 最低被引量
- `filter=primary_location.source.id:SOURCE_ID` — 特定期刊
- `sort=cited_by_count:desc` — 按被引量排序

### 2. 提取元数据

每个结果包含：
- 标题 (title)
- 作者 (authorships[].author.display_name)
- 发表年份 (publication_year)
- 期刊 (primary_location.source.display_name)
- DOI (doi)
- 被引量 (cited_by_count)
- OpenAlex ID (id)

### 3. 下载PDF

OpenAlex提供OA（开放获取）链接：
- 检查 `open_access.is_oa` 字段
- 获取 `open_access.oa_url` 字段
- 如果是OA论文，直接下载PDF

### 4. 导出引用

支持格式：
- **APA 7th**: 作者. (年份). 标题. 期刊. DOI
- **BibTeX**: 自动生成BibTeX条目
- **GB/T 7714**: 中国标准引用格式

## 使用示例

### 搜索示例

```
用户：帮我搜一下多智能体编队控制的论文
→ 调用OpenAlex API搜索 "multi-agent formation control"
→ 返回top 10结果，按被引量排序
→ 展示标题、作者、年份、被引量、期刊
```

### 下载PDF示例

```
用户：这篇论文能下载吗？DOI: 10.1109/tie.2017.2701778
→ 检查OpenAlex的open_access字段
→ 如果是OA，提供下载链接
→ 如果不是OA，建议其他获取方式
```

### 引用导出示例

```
用户：帮我生成这篇论文的APA引用
→ 解析元数据
→ 生成APA 7th格式：
  Ge, X., & Han, Q.-L. (2017). Distributed Formation Control...
  IEEE Transactions on Industrial Electronics. https://doi.org/...
```

## API调用脚本

### 搜索函数

```bash
search_papers() {
    local query="$1"
    local limit="${2:-10}"
    local year_filter="${3:-}"
    
    local url="https://api.openalex.org/works?search=${query}&per_page=${limit}"
    
    if [ -n "$year_filter" ]; then
        url="${url}&filter=publication_year:${year_filter}"
    fi
    
    curl -s "$url" | python3 -c "
import json, sys
d = json.load(sys.stdin)
for i, w in enumerate(d.get('results', []), 1):
    authors = ', '.join([a['author'].get('display_name','') for a in w.get('authorships',[])[:3]])
    if len(w.get('authorships',[])) > 3:
        authors += ' et al.'
    source = ''
    if w.get('primary_location',{}).get('source'):
        source = w['primary_location']['source'].get('display_name','')
    print(f\"{i}. {w.get('title','')}\")
    print(f\"   作者: {authors}\")
    print(f\"   年份: {w.get('publication_year','')}\")
    print(f\"   期刊: {source}\")
    print(f\"   被引: {w.get('cited_by_count',0)}\")
    print(f\"   DOI: {w.get('doi','')}\")
    oa = w.get('open_access',{})
    if oa.get('is_oa'):
        print(f\"   PDF: {oa.get('oa_url','')}\")
    print()
"
}
```

### 获取论文详情

```bash
get_paper_by_doi() {
    local doi="$1"
    curl -s "https://api.openalex.org/works/doi:${doi}"
}
```

### 生成APA引用

```bash
generate_apa() {
    local doi="$1"
    curl -s "https://api.openalex.org/works/doi:${doi}" | python3 -c "
import json, sys
w = json.load(sys.stdin)
authors = []
for a in w.get('authorships', []):
    name = a['author'].get('display_name', '')
    parts = name.split()
    if len(parts) >= 2:
        authors.append(f'{parts[-1]}, {parts[0][0]}.')
    else:
        authors.append(name)
author_str = ', '.join(authors[:7])
if len(w.get('authorships', [])) > 7:
    author_str += ', ...'
year = w.get('publication_year', 'n.d.')
title = w.get('title', 'Untitled')
source = ''
if w.get('primary_location',{}).get('source'):
    source = w['primary_location']['source'].get('display_name','')
doi = w.get('doi', '')
print(f'{author_str} ({year}). {title}. {source}. {doi}')
"
}
```

## 与百度学术的配合

对于知网独有（OpenAlex未收录）的论文，建议：
1. 先用OpenAlex搜索（数据更结构化）
2. 如果没找到，用 `baidu-scholar-search` 补充
3. 两者结合基本覆盖所有中英文论文

## 限制

- OpenAlex的中文论文覆盖不如英文完整
- 部分中文论文缺少DOI
- 被引量数据来自Crossref，可能与知网有差异
- 不支持直接下载知网PDF（需要机构访问权限）

## 文件结构

```
cnki-scholar/
├── SKILL.md
└── references/
    ├── openalex-fields.md    # OpenAlex字段说明
    └── citation-formats.md   # 引用格式模板
```
