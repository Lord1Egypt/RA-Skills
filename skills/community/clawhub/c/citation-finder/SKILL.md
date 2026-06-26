---
name: citation-finder
description: Academic citation lookup and formatter. Given a fuzzy paper title (Chinese or English), searches CrossRef, Semantic Scholar, Baidu Scholar, and CNKI, then returns GB/T 7714, APA 7th, and MLA 9th formatted citations with source links.
---

# Citation Finder Skill

## Description

Academic citation lookup and formatter. Given a fuzzy paper title or description (in Chinese or English), searches both Chinese and English academic databases, identifies the most likely paper, and returns formatted citations in GB/T 7714, APA, and MLA formats along with source links.

## Trigger Conditions

Use this skill when the user:
- Asks to find a paper or citation (e.g. "帮我找这篇文献", "cite this paper", "这篇论文怎么引用")
- Provides a fuzzy or partial paper title in Chinese or English
- Asks to format a reference in GB/T 7714, APA, or MLA
- Uses keywords: 参考文献, 引用格式, 文献查找, find paper, citation, reference, cite

## Workflow

1. Detect input language (Chinese / English / mixed)
2. Search **in parallel**:
   - English: CrossRef API + Semantic Scholar API
   - Chinese: Baidu Scholar (web scrape) + CNKI search
3. Score and rank candidates by title similarity + metadata completeness
4. If top match confidence > 80%: return directly
5. If confidence 50–80%: show top 3 candidates, ask user to confirm
6. If confidence < 50%: inform user and ask for more details
7. Format confirmed paper into GB/T 7714, APA 7th, MLA 9th
8. Return citations + DOI/source URL

## Usage

```
用法：直接描述或粘贴模糊文献标题
示例：帮我找一下 "注意力机制在自然语言处理中的应用" 这篇论文的引用格式
示例：find citation for "attention is all you need"
```

## Scripts

- `scripts/search_en.py` — CrossRef + Semantic Scholar search
- `scripts/search_cn.py` — Baidu Scholar + CNKI search  
- `scripts/format_cite.py` — Citation formatter (GB/T 7714, APA, MLA)
- `scripts/run.py` — Main entry point (orchestrates all steps)

## Dependencies

```
requests>=2.28.0
beautifulsoup4>=4.11.0
rapidfuzz>=3.0.0
```

Install: `pip install requests beautifulsoup4 rapidfuzz`
