---
name: AntV文档协议服务
description: 为AI开发和QA设计的模型上下文协议服务器，提供AntV文档上下文和代码示例。
version: 1.0.0
---

# AntV文档协议服务

为AI开发和QA设计的模型上下文协议服务器，提供AntV文档上下文和代码示例。

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
| AntV Intelligent Assistant Preprocessing Tool - Specifically designed to handle any user queries related to AntV visualization libraries.
  This tool is the first step in processing AntV technology stack issues, responsible for intelligently identifying, parsing, and structuring user visualization requirements.

**MANDATORY: Must be called for ANY new AntV-related queries, including simple questions. Always precedes query_antv_document tool.**

When to use this tool:
- **AntV-related queries**: Questions about g2/g6/l7/x6/f2/s2/g/ava/adc libraries.
- **Visualization tasks**: Creating charts, graphs, maps, or other visualizations.
- **Problem solving**: Debugging errors, performance issues, or compatibility problems.
- **Learning & implementation**: Understanding concepts or requesting code examples.

Key features:
- **Smart Library Detection**: Scans installed AntV libraries and recommends the best fit based on query and project dependencies.
- **Topic & Intent Extraction**: Intelligently extracts technical topics and determines user intent (implement/solve).
- **Task Complexity Handling**: Detects complex tasks and decomposes them into manageable subtasks.
- **Seamless Integration**: Prepares structured data for the query_antv_document tool to provide precise solutions. | `scripts.tools.extract_antv_topic` |
| AntV Context Retrieval Assistant - Fetches relevant documentation, code examples, and best practices from official AntV resources. Supports g2, g6, l7, x6, f2, s2, g, ava, adc libraries, and handles subtasks iterative queries.

**MANDATORY: Must be called for ANY AntV-related query (g2, g6, l7, x6, f2, s2, g, ava, adc), regardless of task complexity. No exceptions for simple tasks.**

When to use this tool:
- **Implementation & Optimization**: To implement new features, modify styles, refactor code, or optimize performance in AntV solutions.
- **Debugging & Problem Solving**: For troubleshooting errors, unexpected behaviors, or technical challenges in AntV projects.
- **Learning & Best Practices**: To explore official documentation, code examples, design patterns, or advanced features.
- **Complex Task Handling**: For multi-step tasks requiring subtask decomposition (e.g., "Build a dashboard with interactive charts").
- **Simple modifications**: Even basic changes like "Change the chart's color" or "Update legend position" in AntV context. | `scripts.tools.query_antv_document` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.extract_antv_topic
工具描述：AntV Intelligent Assistant Preprocessing Tool - Specifically designed to handle any user queries related to AntV visualization libraries.
  This tool is the first step in processing AntV technology stack issues, responsible for intelligently identifying, parsing, and structuring user visualization requirements.

**MANDATORY: Must be called for ANY new AntV-related queries, including simple questions. Always precedes query_antv_document tool.**

When to use this tool:
- **AntV-related queries**: Questions about g2/g6/l7/x6/f2/s2/g/ava/adc libraries.
- **Visualization tasks**: Creating charts, graphs, maps, or other visualizations.
- **Problem solving**: Debugging errors, performance issues, or compatibility problems.
- **Learning & implementation**: Understanding concepts or requesting code examples.

Key features:
- **Smart Library Detection**: Scans installed AntV libraries and recommends the best fit based on query and project dependencies.
- **Topic & Intent Extraction**: Intelligently extracts technical topics and determines user intent (implement/solve).
- **Task Complexity Handling**: Detects complex tasks and decomposes them into manageable subtasks.
- **Seamless Integration**: Prepares structured data for the query_antv_document tool to provide precise solutions.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |User specific question or requirement description|
|library|string|false| |AntV library name (optional) - If not specified, tool will automatically detect project dependencies and intelligently recommend|
|maxTopics|integer|false|5.0|Maximum number of extracted topic keywords, default 5, can be increased appropriately for complex tasks|

---

## scripts.tools.query_antv_document
工具描述：AntV Context Retrieval Assistant - Fetches relevant documentation, code examples, and best practices from official AntV resources. Supports g2, g6, l7, x6, f2, s2, g, ava, adc libraries, and handles subtasks iterative queries.

**MANDATORY: Must be called for ANY AntV-related query (g2, g6, l7, x6, f2, s2, g, ava, adc), regardless of task complexity. No exceptions for simple tasks.**

When to use this tool:
- **Implementation & Optimization**: To implement new features, modify styles, refactor code, or optimize performance in AntV solutions.
- **Debugging & Problem Solving**: For troubleshooting errors, unexpected behaviors, or technical challenges in AntV projects.
- **Learning & Best Practices**: To explore official documentation, code examples, design patterns, or advanced features.
- **Complex Task Handling**: For multi-step tasks requiring subtask decomposition (e.g., "Build a dashboard with interactive charts").
- **Simple modifications**: Even basic changes like "Change the chart's color" or "Update legend position" in AntV context.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|library|string|true| |Specified AntV library type, intelligently identified based on user query|
|query|string|true| |User specific question or requirement description|
|topic|string|true| |Technical topic keywords (comma-separated). Provided by `extract_antv_topic` or directly extracted from simple questions.|
|intent|string|true| |Extracted user intent, provided by extract_antv_topic tool or directly extracted from simple questions.|
|tokens|integer|false|5000.0|tokens for returned content|
|subTasks|array|false| |Decomposed subtask list for complex tasks, supports batch processing|

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