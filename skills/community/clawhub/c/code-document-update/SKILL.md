---
name: 代码文档更新服务
description: Context7 MCP 是一款为开发者提供最新代码文档和示例的服务，通过集成到开发环境中，确保LLM生成的代码基于最新的库文档。
version: 1.0.0
---

# 代码文档更新服务

Context7 MCP 是一款为开发者提供最新代码文档和示例的服务，通过集成到开发环境中，确保LLM生成的代码基于最新的库文档。

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
| Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries.

You MUST call this function before 'get-library-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

Selection Process:
1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
- Name similarity to the query (exact matches prioritized)
- Description relevance to the query's intent
- Documentation coverage (prioritize libraries with higher Code Snippet counts)
- Source reputation (consider libraries with High or Medium reputation more authoritative)
- Benchmark Score: Quality indicator (100 is the highest score)

Response Format:
- Return the selected library ID in a clearly marked section
- Provide a brief explanation for why this library was chosen
- If multiple good matches exist, acknowledge this but proceed with the most relevant one
- If no good matches exist, clearly state this and suggest query refinements

For ambiguous queries, request clarification before proceeding with a best-guess match. | `scripts.tools.resolve_library_id` |
| Fetches up-to-date documentation for a library. You must call 'resolve-library-id' first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query. Use mode='code' (default) for API references and code examples, or mode='info' for conceptual guides, narrative information, and architectural questions. | `scripts.tools.get_library_docs` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.resolve_library_id
工具描述：Resolves a package/product name to a Context7-compatible library ID and returns a list of matching libraries.

You MUST call this function before 'get-library-docs' to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

Selection Process:
1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
- Name similarity to the query (exact matches prioritized)
- Description relevance to the query's intent
- Documentation coverage (prioritize libraries with higher Code Snippet counts)
- Source reputation (consider libraries with High or Medium reputation more authoritative)
- Benchmark Score: Quality indicator (100 is the highest score)

Response Format:
- Return the selected library ID in a clearly marked section
- Provide a brief explanation for why this library was chosen
- If multiple good matches exist, acknowledge this but proceed with the most relevant one
- If no good matches exist, clearly state this and suggest query refinements

For ambiguous queries, request clarification before proceeding with a best-guess match.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|libraryName|string|true| |Library name to search for and retrieve a Context7-compatible library ID.|

---

## scripts.tools.get_library_docs
工具描述：Fetches up-to-date documentation for a library. You must call 'resolve-library-id' first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query. Use mode='code' (default) for API references and code examples, or mode='info' for conceptual guides, narrative information, and architectural questions.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|context7CompatibleLibraryID|string|true| |Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v14.3.0-canary.87') retrieved from 'resolve-library-id' or directly from user query in the format '/org/project' or '/org/project/version'.|
|mode|string|false|"code"|Documentation mode: 'code' for API references and code examples (default), 'info' for conceptual guides, narrative information, and architectural questions.|
|topic|string|false| |Topic to focus documentation on (e.g., 'hooks', 'routing').|
|page|integer|false| |Page number for pagination (start: 1, default: 1). If the context is not sufficient, try page=2, page=3, page=4, etc. with the same topic.|

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