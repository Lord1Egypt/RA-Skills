---
name: 动态提示生成服务
description: Mercury Spec Ops MCP Server 是一个基于模块化架构的动态提示生成和模板组装工具，适用于AI助手与专业内容的交互，支持31种技术栈、10种分析维度和34个模板部分的动态生成。
version: 1.0.0
---

# 动态提示生成服务

Mercury Spec Ops MCP Server 是一个基于模块化架构的动态提示生成和模板组装工具，适用于AI助手与专业内容的交互，支持31种技术栈、10种分析维度和34个模板部分的动态生成。

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
| Generate an assembled Product Requirements Document prompt with specified technology stacks and analysis focus areas | `scripts.tools.generate_prd_prompt` |
| Generate an assembled codebase analysis prompt with specified technology stacks and analysis focus areas | `scripts.tools.generate_codebase_analysis_prompt` |
| Generate an assembled bug analysis prompt with specified technology stacks and severity level | `scripts.tools.generate_bug_analysis_prompt` |
| Fetch a comprehensive Product Requirements Document markdown template with all standard sections (14 sections total) | `scripts.tools.get_prd_template` |
| Fetch a comprehensive codebase analysis markdown template with all standard sections (12 sections total) | `scripts.tools.get_codebase_analysis_template` |
| Fetch a comprehensive bug analysis markdown template with all standard sections (8 sections total) | `scripts.tools.get_bug_analysis_template` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.generate_prd_prompt
工具描述：Generate an assembled Product Requirements Document prompt with specified technology stacks and analysis focus areas
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|technology_stack|array|true| |Technology stacks to include in prompt assembly|
|analysis_focus|array|false| |Analysis focus areas for the PRD|
|project_context|string|false| |Optional project context or background information|

---

## scripts.tools.generate_codebase_analysis_prompt
工具描述：Generate an assembled codebase analysis prompt with specified technology stacks and analysis focus areas
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|technology_stack|array|true| |Technology stacks to analyze|
|analysis_focus|array|true| |Areas to focus analysis on|

---

## scripts.tools.generate_bug_analysis_prompt
工具描述：Generate an assembled bug analysis prompt with specified technology stacks and severity level
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|technology_stack|array|true| |Technology stacks involved in the bug|
|severity|string|true| |Bug severity level|
|bug_context|string|false| |Optional bug description or context|

---

## scripts.tools.get_prd_template
工具描述：Fetch a comprehensive Product Requirements Document markdown template with all standard sections (14 sections total)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_codebase_analysis_template
工具描述：Fetch a comprehensive codebase analysis markdown template with all standard sections (12 sections total)
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.get_bug_analysis_template
工具描述：Fetch a comprehensive bug analysis markdown template with all standard sections (8 sections total)
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