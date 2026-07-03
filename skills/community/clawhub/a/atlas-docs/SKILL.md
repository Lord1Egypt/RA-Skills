---
name: 文档处理服务
description: Atlas Docs MCP服务器为AI助手提供库和框架的技术文档，将官方文档处理为适合LLM使用的Markdown版本，适用于Cursor、Cline、Windsurf等MCP兼容的LLM客户端。
version: 1.0.0
---

# 文档处理服务

Atlas Docs MCP服务器为AI助手提供库和框架的技术文档，将官方文档处理为适合LLM使用的Markdown版本，适用于Cursor、Cline、Windsurf等MCP兼容的LLM客户端。

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
| Lists all available documentation libraries and frameworks. Use this as your first step to discover available documentation sets. Returns name, description and source url for each documentation set. Required before using other documentation tools since you need the docName. | `scripts.tools.list_docs` |
| Searches a documentation set for specific content. Use this to find pages containing particular keywords, concepts, or topics. Returns matching pages ranked by relevance with their paths and descriptions. Follow up with get_docs_page to get full content. | `scripts.tools.search_docs` |
| Retrieves a condensed, LLM-friendly index of the pages in a documentation set. Use this for initial exploration to understand what's covered and identify relevant pages. Returns a markdown page with a list of available pages. Follow up with get_docs_page to get full content. | `scripts.tools.get_docs_index` |
| Retrieves a specific documentation page's content using its relative path. Use this to get detailed information about a known topic, after identifying the relevant page through get_docs_index or search_docs. Returns the complete content of a single documentation page. | `scripts.tools.get_docs_page` |
| Retrieves the complete documentation content in a single consolidated file. Use this when you need comprehensive knowledge or need to analyze the full documentation context. Returns a large volume of text - consider using get_docs_page or search_docs for targeted information. | `scripts.tools.get_docs_full` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.list_docs
工具描述：Lists all available documentation libraries and frameworks. Use this as your first step to discover available documentation sets. Returns name, description and source url for each documentation set. Required before using other documentation tools since you need the docName.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.search_docs
工具描述：Searches a documentation set for specific content. Use this to find pages containing particular keywords, concepts, or topics. Returns matching pages ranked by relevance with their paths and descriptions. Follow up with get_docs_page to get full content.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|docName|string|true| |Name of the documentation set|
|query|string|true| |Search query to find relevant pages within the documentation set|

---

## scripts.tools.get_docs_index
工具描述：Retrieves a condensed, LLM-friendly index of the pages in a documentation set. Use this for initial exploration to understand what's covered and identify relevant pages. Returns a markdown page with a list of available pages. Follow up with get_docs_page to get full content.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|docName|string|true| |Name of the documentation set|

---

## scripts.tools.get_docs_page
工具描述：Retrieves a specific documentation page's content using its relative path. Use this to get detailed information about a known topic, after identifying the relevant page through get_docs_index or search_docs. Returns the complete content of a single documentation page.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|docName|string|true| |Name of the documentation set|
|pagePath|string|true| |The root-relative path of the specific documentation page (e.g., '/guides/getting-started', '/api/authentication')|

---

## scripts.tools.get_docs_full
工具描述：Retrieves the complete documentation content in a single consolidated file. Use this when you need comprehensive knowledge or need to analyze the full documentation context. Returns a large volume of text - consider using get_docs_page or search_docs for targeted information.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|docName|string|true| |Name of the documentation set|

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