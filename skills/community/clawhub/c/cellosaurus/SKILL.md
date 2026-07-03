---
name: 细胞系知识资源服务
description: Cellosaurus MCP Server是一个非官方的模型上下文协议服务器，用于访问SIB Cellosaurus细胞系知识资源，提供细胞系搜索、详细信息获取和数据库版本信息等功能。
version: 1.0.0
---

# 细胞系知识资源服务

Cellosaurus MCP Server是一个非官方的模型上下文协议服务器，用于访问SIB Cellosaurus细胞系知识资源，提供细胞系搜索、详细信息获取和数据库版本信息等功能。

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
| Search for cell lines in the Cellosaurus database.

Use Solr search syntax to find cell lines by various criteria.

Examples
--------
- Basic name search: "id:HeLa" or "sy:HeLa"
- Species filter: "ox:human" or "ox:9606"
- Disease filter: "di:cancer" or "di:hepatoblastoma"
- Combined: "ox:human di:cancer ca:cancer"
- Site filter: "derived-from-site:liver"

Args:
    query: Search query using Solr syntax (default: "id:HeLa")
    fields: List of fields to return (e.g., ["id", "ac", "ox", "di"])
    start: Starting index for pagination (default: 0)
    rows: Number of results to return (default: 10, max: 1000)
    sort_order: Sort order (e.g., "group asc,derived-from-site desc")

Returns
-------
    Dictionary containing search results with cell line information | `scripts.tools.search_cell_lines` |
| Get detailed information about a specific cell line by its accession number.

Args:
    accession: Cell line accession number (e.g., "CVCL_0030" for HeLa)
    fields: List of specific fields to return (e.g., ["id", "ac", "str", "di"])

Returns
-------
    Dictionary containing detailed cell line information | `scripts.tools.get_cell_line_info` |
| Get information about the current Cellosaurus database release.

Returns
-------
    Dictionary containing release version, date, and statistics | `scripts.tools.get_release_info` |
| Find cell lines derived from patients with a specific disease.

Args:
    disease: Disease name or term (e.g., "hepatoblastoma", "cancer", "leukemia")
    species: Species filter (default: "human", can be "mouse", "rat", etc.)
    fields: Specific fields to return
    limit: Maximum number of results (default: 10)

Returns
-------
    Dictionary containing cell lines associated with the disease | `scripts.tools.find_cell_lines_by_disease` |
| Find cell lines derived from a specific tissue or organ.

Args:
    tissue: Tissue/organ name (e.g., "liver", "lung", "breast", "brain")
    species: Species filter (default: "human")
    fields: Specific fields to return
    limit: Maximum number of results (default: 10)

Returns
-------
    Dictionary containing cell lines from the specified tissue | `scripts.tools.find_cell_lines_by_tissue` |
| Get a list of all available fields that can be requested from the Cellosaurus API.

Returns
-------
    Dictionary mapping field names to their descriptions | `scripts.tools.list_available_fields` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.search_cell_lines
工具描述：Search for cell lines in the Cellosaurus database.

Use Solr search syntax to find cell lines by various criteria.

Examples
--------
- Basic name search: "id:HeLa" or "sy:HeLa"
- Species filter: "ox:human" or "ox:9606"
- Disease filter: "di:cancer" or "di:hepatoblastoma"
- Combined: "ox:human di:cancer ca:cancer"
- Site filter: "derived-from-site:liver"

Args:
    query: Search query using Solr syntax (default: "id:HeLa")
    fields: List of fields to return (e.g., ["id", "ac", "ox", "di"])
    start: Starting index for pagination (default: 0)
    rows: Number of results to return (default: 10, max: 1000)
    sort_order: Sort order (e.g., "group asc,derived-from-site desc")

Returns
-------
    Dictionary containing search results with cell line information
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|false|"id:HeLa"|null|
|fields|null|false| |null|
|start|integer|false|0.0|null|
|rows|integer|false|10.0|null|
|sort_order|null|false| |null|

---

## scripts.tools.get_cell_line_info
工具描述：Get detailed information about a specific cell line by its accession number.

Args:
    accession: Cell line accession number (e.g., "CVCL_0030" for HeLa)
    fields: List of specific fields to return (e.g., ["id", "ac", "str", "di"])

Returns
-------
    Dictionary containing detailed cell line information
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|accession|string|true| |null|
|fields|null|false| |null|

---

## scripts.tools.get_release_info
工具描述：Get information about the current Cellosaurus database release.

Returns
-------
    Dictionary containing release version, date, and statistics
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.find_cell_lines_by_disease
工具描述：Find cell lines derived from patients with a specific disease.

Args:
    disease: Disease name or term (e.g., "hepatoblastoma", "cancer", "leukemia")
    species: Species filter (default: "human", can be "mouse", "rat", etc.)
    fields: Specific fields to return
    limit: Maximum number of results (default: 10)

Returns
-------
    Dictionary containing cell lines associated with the disease
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|disease|string|true| |null|
|species|string|false|"human"|null|
|fields|null|false| |null|
|limit|integer|false|10.0|null|

---

## scripts.tools.find_cell_lines_by_tissue
工具描述：Find cell lines derived from a specific tissue or organ.

Args:
    tissue: Tissue/organ name (e.g., "liver", "lung", "breast", "brain")
    species: Species filter (default: "human")
    fields: Specific fields to return
    limit: Maximum number of results (default: 10)

Returns
-------
    Dictionary containing cell lines from the specified tissue
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tissue|string|true| |null|
|species|string|false|"human"|null|
|fields|null|false| |null|
|limit|integer|false|10.0|null|

---

## scripts.tools.list_available_fields
工具描述：Get a list of all available fields that can be requested from the Cellosaurus API.

Returns
-------
    Dictionary mapping field names to their descriptions
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

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