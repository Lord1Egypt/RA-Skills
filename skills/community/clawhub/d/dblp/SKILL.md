---
name: 学术文献检索与引用工具
description: 一个通过模型上下文协议（MCP）提供DBLP计算机科学文献数据库访问的服务，支持学术文献检索、引用生成及格式化功能。
version: 1.0.0
---

# 学术文献检索与引用工具

一个通过模型上下文协议（MCP）提供DBLP计算机科学文献数据库访问的服务，支持学术文献检索、引用生成及格式化功能。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Get detailed DBLP usage instructions. Key points:
- Batch searches in parallel (5-10 at a time) for efficiency
- Add entries immediately after each search result (don't batch add_bibtex_entry calls)
- Use author+year for best results: search('Vaswani 2017') not just title
- Copy dblp_key EXACTLY from search results to add_bibtex_entry
- Export once at the end with export_bibtex
Call this tool for complete workflow details, search strategies, and examples. | `scripts.tools.get_instructions` |
| Search DBLP for publications using a boolean query string.
Arguments:
  - query (string, required): A query string that may include boolean operators 'and' and 'or' (case-insensitive).
    For example, 'Swin and Transformer'. Parentheses are not supported.
  - max_results (number, optional): Maximum number of publications to return. Default is 10.
  - year_from (number, optional): Lower bound for publication year.
  - year_to (number, optional): Upper bound for publication year.
  - venue_filter (string, optional): Case-insensitive substring filter for publication venues (e.g., 'iclr').
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a list of publication objects including title, authors, venue, year, type, doi, ee, and url. | `scripts.tools.search` |
| Search DBLP for publications with fuzzy title matching.
Arguments:
  - title (string, required): Full or partial title of the publication (case-insensitive).
  - similarity_threshold (number, required): A float between 0 and 1 where 1.0 means an exact match.
  - max_results (number, optional): Maximum number of publications to return. Default is 10.
  - year_from (number, optional): Lower bound for publication year.
  - year_to (number, optional): Upper bound for publication year.
  - venue_filter (string, optional): Case-insensitive substring filter for publication venues.
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a list of publication objects sorted by title similarity score. | `scripts.tools.fuzzy_title_search` |
| Retrieve publication details for a specific author with fuzzy matching.
Arguments:
  - author_name (string, required): Full or partial author name (case-insensitive).
  - similarity_threshold (number, required): A float between 0 and 1 where 1.0 means an exact match.
  - max_results (number, optional): Maximum number of publications to return. Default is 20.
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a dictionary with keys: name, publication_count, publications, and stats (which includes top venues, years, and types). | `scripts.tools.get_author_publications` |
| Retrieve information about a publication venue from DBLP.
Arguments:
  - venue_name (string, required): Venue name or abbreviation (e.g., 'ICLR', 'NeurIPS', or full name).
Returns a dictionary with fields:
  - venue: Full venue title
  - acronym: Venue acronym/abbreviation (if available)
  - type: Venue type (e.g., 'Conference or Workshop', 'Journal', 'Repository')
  - url: Canonical DBLP URL for the venue
Note: Publisher, ISSN, and other metadata are not available through this endpoint. | `scripts.tools.get_venue_info` |
| Calculate statistics from a list of publication results.
Arguments:
  - results (array, required): An array of publication objects, each with at least 'title', 'authors', 'venue', and 'year'.
Returns a dictionary with:
  - total_publications: Total count.
  - time_range: Dictionary with 'min' and 'max' publication years.
  - top_authors: List of tuples (author, count) sorted by count.
  - top_venues: List of tuples (venue, count) sorted by count (empty venue is treated as '(empty)'). | `scripts.tools.calculate_statistics` |
| Add a BibTeX entry to the collection for later export. Call this once for each paper you want to export.
Arguments:
  - dblp_key (string, required): The DBLP key from search results (e.g., 'conf/nips/VaswaniSPUJGKP17').
  - citation_key (string, required): The citation key to use in the .bib file (e.g., 'Vaswani2017').
Workflow:
  1. Fetches BibTeX directly from DBLP using the provided key
  2. Replaces the citation key with your custom key
  3. Adds to collection (duplicate citation_key will be overwritten)
  4. Returns count of entries currently in collection
After adding all entries, call export_bibtex to save them to a .bib file. | `scripts.tools.add_bibtex_entry` |
| Export all collected BibTeX entries to a .bib file. Call this after adding all entries with add_bibtex_entry.
Workflow:
  1. Saves all collected entries to a .bib file at the specified path
  2. Clears the collection for next export
  3. Returns the full path to the exported file
Returns error if no entries have been added yet. | `scripts.tools.export_bibtex` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.get_instructions
工具描述：Get detailed DBLP usage instructions. Key points:
- Batch searches in parallel (5-10 at a time) for efficiency
- Add entries immediately after each search result (don't batch add_bibtex_entry calls)
- Use author+year for best results: search('Vaswani 2017') not just title
- Copy dblp_key EXACTLY from search results to add_bibtex_entry
- Export once at the end with export_bibtex
Call this tool for complete workflow details, search strategies, and examples.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.search
工具描述：Search DBLP for publications using a boolean query string.
Arguments:
  - query (string, required): A query string that may include boolean operators 'and' and 'or' (case-insensitive).
    For example, 'Swin and Transformer'. Parentheses are not supported.
  - max_results (number, optional): Maximum number of publications to return. Default is 10.
  - year_from (number, optional): Lower bound for publication year.
  - year_to (number, optional): Upper bound for publication year.
  - venue_filter (string, optional): Case-insensitive substring filter for publication venues (e.g., 'iclr').
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a list of publication objects including title, authors, venue, year, type, doi, ee, and url.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |null|
|max_results|number|false| |null|
|year_from|number|false| |null|
|year_to|number|false| |null|
|venue_filter|string|false| |null|
|include_bibtex|boolean|false| |null|

---

## scripts.tools.fuzzy_title_search
工具描述：Search DBLP for publications with fuzzy title matching.
Arguments:
  - title (string, required): Full or partial title of the publication (case-insensitive).
  - similarity_threshold (number, required): A float between 0 and 1 where 1.0 means an exact match.
  - max_results (number, optional): Maximum number of publications to return. Default is 10.
  - year_from (number, optional): Lower bound for publication year.
  - year_to (number, optional): Upper bound for publication year.
  - venue_filter (string, optional): Case-insensitive substring filter for publication venues.
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a list of publication objects sorted by title similarity score.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|title|string|true| |null|
|similarity_threshold|number|true| |null|
|max_results|number|false| |null|
|year_from|number|false| |null|
|year_to|number|false| |null|
|venue_filter|string|false| |null|
|include_bibtex|boolean|false| |null|

---

## scripts.tools.get_author_publications
工具描述：Retrieve publication details for a specific author with fuzzy matching.
Arguments:
  - author_name (string, required): Full or partial author name (case-insensitive).
  - similarity_threshold (number, required): A float between 0 and 1 where 1.0 means an exact match.
  - max_results (number, optional): Maximum number of publications to return. Default is 20.
  - include_bibtex (boolean, optional): Whether to include BibTeX entries in the results. Default is false.
Returns a dictionary with keys: name, publication_count, publications, and stats (which includes top venues, years, and types).
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|author_name|string|true| |null|
|similarity_threshold|number|true| |null|
|max_results|number|false| |null|
|include_bibtex|boolean|false| |null|

---

## scripts.tools.get_venue_info
工具描述：Retrieve information about a publication venue from DBLP.
Arguments:
  - venue_name (string, required): Venue name or abbreviation (e.g., 'ICLR', 'NeurIPS', or full name).
Returns a dictionary with fields:
  - venue: Full venue title
  - acronym: Venue acronym/abbreviation (if available)
  - type: Venue type (e.g., 'Conference or Workshop', 'Journal', 'Repository')
  - url: Canonical DBLP URL for the venue
Note: Publisher, ISSN, and other metadata are not available through this endpoint.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|venue_name|string|true| |null|

---

## scripts.tools.calculate_statistics
工具描述：Calculate statistics from a list of publication results.
Arguments:
  - results (array, required): An array of publication objects, each with at least 'title', 'authors', 'venue', and 'year'.
Returns a dictionary with:
  - total_publications: Total count.
  - time_range: Dictionary with 'min' and 'max' publication years.
  - top_authors: List of tuples (author, count) sorted by count.
  - top_venues: List of tuples (venue, count) sorted by count (empty venue is treated as '(empty)').
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|results|array|true| |null|

---

## scripts.tools.add_bibtex_entry
工具描述：Add a BibTeX entry to the collection for later export. Call this once for each paper you want to export.
Arguments:
  - dblp_key (string, required): The DBLP key from search results (e.g., 'conf/nips/VaswaniSPUJGKP17').
  - citation_key (string, required): The citation key to use in the .bib file (e.g., 'Vaswani2017').
Workflow:
  1. Fetches BibTeX directly from DBLP using the provided key
  2. Replaces the citation key with your custom key
  3. Adds to collection (duplicate citation_key will be overwritten)
  4. Returns count of entries currently in collection
After adding all entries, call export_bibtex to save them to a .bib file.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|dblp_key|string|true| |null|
|citation_key|string|true| |null|

---

## scripts.tools.export_bibtex
工具描述：Export all collected BibTeX entries to a .bib file. Call this after adding all entries with add_bibtex_entry.
Workflow:
  1. Saves all collected entries to a .bib file at the specified path
  2. Clears the collection for next export
  3. Returns the full path to the exported file
Returns error if no entries have been added yet.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|path|string|true| |Absolute path for the .bib file (e.g., '/path/to/refs.bib'). The .bib extension is added automatically if missing. Parent directories are created if needed.|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据