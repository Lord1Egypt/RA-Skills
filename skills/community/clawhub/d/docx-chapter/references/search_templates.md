# Mandatory Search Templates (Phase 5 Pass 2)

> 借鉴 citation-check v2 §Mandatory Search Templates。按声明类型分 5 组模板，每组 3-5 条查询。Pass 2 验证时全量运行，不全量跑完不定论。

## 1. Academic Citations

用于验证 Attribution 类型声明（引用论文/报告/研究）。

```
Query 1: "{first author last name} {year} {first 3 words of title}"
Query 2: "{full paper title}" site:semanticscholar.org OR site:arxiv.org
Query 3: "{first author} {year} {venue/journal name}"
Query 4: "doi:{DOI}" (if DOI provided in footnote)
Query 5: "arxiv:{arxiv_id}" (if arXiv ID provided)
```

**判定**：2 条以上返回匹配结果 → 引用存在。0 条 → Citation Not Found。

## 2. Statistics

用于验证 Statistic 类型声明（市场规模、使用量、行业数据）。

```
Query 1: "{exact number with unit} {topic} {year}"
Query 2: "{topic} {year} statistics report site:statista.com"
Query 3: "{topic} {year} report site:mckinsey.com OR site:gartner.com"
Query 4: "{topic} market size {year} site:gov OR site:edu"
Query 5: "{topic} {number} original source"
```

## 3. Company / Product Claims

```
Query 1: "{company name} {claim topic} press release {year}"
Query 2: "site:{company domain} {claim topic}"
Query 3: "{company name} {metric} official announcement"
Query 4: "{company name} {claim} SEC filing" (for public companies)
```

## 4. Health / Medical Claims

```
Query 1: "{claim topic} site:who.int OR site:cdc.gov OR site:nih.gov"
Query 2: "{claim} systematic review site:cochrane.org"
Query 3: "{claim} meta-analysis pubmed"
```

## 5. Government / Policy Claims

```
Query 1: "{policy/law name} site:gov"
Query 2: "{statistic} official statistics {country}"
Query 3: "{claim} {agency name} report"
```

## 在 Phase 2 搜索研究中的复用

Phase 2 的 unified_search + Tavily Research 结果作为缓存：
- 若 Pass 2 的搜索模板查询在 Phase 2 结果中已有覆盖 → 复用，标注 `source: phase2_cache`
- 若未覆盖 → 独立执行搜索

## 搜索工具选择

| 工具 | 适用 | 说明 |
|------|------|------|
| `/unified_search` (三引擎) | 通用 | Exa + Google + Tavily 聚合，URL 准确性高 |
| Tavily Research | 深度 | 长报告级搜索，补充覆盖面 |
| `/tavily_research` (Tavily search) | 快速 | 轻量搜索，适合 3-5 条快速查询 |
