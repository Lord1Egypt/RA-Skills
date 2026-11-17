# Dify DSL 节点类型 → 代码映射参考

Dify 导出的 DSL 是 YAML，顶层结构：`app`（元数据）、`kind: app`、`version`、`workflow.graph.{nodes,edges}`、`workflow.environment_variables`、`dependencies`（插件依赖）。节点配置在 `node.data` 下，`node.data.type` 决定语义。变量引用语法：`{{#node_id.output_var#}}`，环境变量 `{{#env.NAME#}}`，密钥 `{{#secret.NAME#}}`。

## 目录

- 输入/输出节点
- 生成类节点
- 逻辑控制节点
- 数据处理节点
- 外部交互节点
- 变量引用解析规则

## 输入/输出节点

| DSL type | 语义 | 代码映射 |
|---|---|---|
| `start` | 定义输入变量 `data.variables[]`（variable/type/required/label/options/default） | 生成项目的 API 入参 schema（如 Pydantic model），required=True 为必填字段 |
| `end` | workflow 模式的输出，`data.outputs[]` 的 `value_selector` 指向其他节点变量 | API 响应体组装 |
| `answer` | chatflow 模式的流式回答，`data.answer` 是模板文本 | SSE/streaming 响应；模板需做变量插值 |

## 生成类节点

| DSL type | 关键配置 | 代码映射 |
|---|---|---|
| `llm` | `model.{provider,name,mode,completion_params}`、`prompt_template[{role,text}]`、`context.variable_selector`、`vision.enabled`、`structured_output` | 对应 provider SDK（openai/anthropic/langchain 等）；prompt 中的 `{{#...#}}` 必须先插值；completion_params 原样透传；需要 provider 的 API Key（缺失信息！） |
| `agent` | `agent_strategy`、`tools[]`、`model` | ReAct/function-calling 循环；工具清单来自 DSL，需逐一确认是否保留 |
| `question-classifier` | `classes[]`、`model` | 小模型分类调用或规则映射；class id 对应出边 sourceHandle |
| `parameter-extractor` | `parameters[]`、`model` | 结构化抽取（JSON schema 输出 + 校验重试） |

## 逻辑控制节点

| DSL type | 关键配置 | 代码映射 |
|---|---|---|
| `if-else` | `conditions[]`（variable_selector/comparison_operator/value）、`logical_operator` | if/elif；出边 `sourceHandle` 为条件 id 或 `"true"/"false"`，路由时按 handle 过滤 |
| `iteration` | `iterator_selector`（数组变量）、内部子图、`output_selector` | for 循环，子图节点在扁平 nodes 列表中，需按迭代体内边集单独执行 |
| `loop` | `loop_variables`、`break_conditions` | while + break 条件求值 |
| `variable-aggregator` | 多路输入聚合 | 取第一个非 None 的上游输出（advanced 模式按组） |

comparison_operator 映射：`contains`→`in`、`not contains`→`not in`、`is`→`==`、`is not`→`!=`、`empty`→`not v`、`not empty`→`bool(v)`、`start with`→`str.startswith`、`end with`→`str.endswith`、`>`/`<`/`≥`/`≤`→数值比较、`exists`/`not exists`→键存在性。

## 数据处理节点

| DSL type | 关键配置 | 代码映射 |
|---|---|---|
| `code` | `code_language`（python3/javascript）、`code`（内联源码）、`outputs` | **直接保留原代码**封装为函数，不要重写逻辑；javascript 代码需用 Node 运行时或请用户确认改写为 Python |
| `template-transform` | `template`（Jinja2 风格 `{{ var }}`） | Jinja2 渲染（Python）或 string template（Node） |
| `variable-assigner` | `items[]` | 写会话变量（有状态服务需会话存储，无状态可降级为上下文变量） |
| `document-extractor` | `variable_selector`（file 类型） | 按 MIME 分派解析器（pdf→pypdf，docx→python-docx，txt→直读） |
| `list-operator` | `filter_conditions` | 数组 filter/sort |

## 外部交互节点

| DSL type | 关键配置 | 代码映射 | 常见缺失信息 |
|---|---|---|---|
| `http-request` | `method/url/headers/params/body/authorization/timeout` | httpx/requests（Python）或 fetch/axios（Node）；URL 与 header 中的变量先插值 | base URL、鉴权 token |
| `knowledge-retrieval` | `dataset_ids[]`、`retrieval_mode`、`multiple_retrieval_config{top_k,score_threshold,reranking_*}` | 向量检索（pgvector/qdrant/chroma）或调用 Dify API 托管检索 | **dataset 内容不随 DSL 导出**，必须问用户：自建向量库 or 调 Dify API，以及语料来源 |
| `tool` | `provider_id/provider_type/tool_name/tool_configurations` | 优先映射为同功能的开源实现或直接 HTTP 调用；插件凭据不随 DSL 导出 | 插件 API Key、是否保留该工具 |

## 变量引用解析规则

1. `{{#node_id.var#}}`：从上游节点的输出变量池取值；`sys.` 前缀（`sys.query`、`sys.user_id`）映射为运行时系统变量。
2. `{{#env.NAME#}}` / `{{#secret.NAME#}}`：映射为进程环境变量，生成 `.env.example` 占位，**绝不硬编码值**。
3. `{{#context#}}`（llm 节点内）：知识检索结果拼接文本。
4. start 节点变量：API 请求体字段；conversation_variables：会话级状态。

## 注意事项

- DSL 版本差异：`version: 0.1.x` 无 `dependencies`；`0.3.x` 有插件市场依赖声明。解析时按字段存在性判断，不依赖版本号。
- chatflow（`mode: advanced-chat`）用 `answer` 节点，生成项目时需决定流式 or 一次性返回（问用户或默认流式 SSE）。
- `dependencies` 里的 marketplace 插件（如 `langgenius/openai`）只声明 provider，凭据在 Dify 实例里，代码化后全部转为环境变量。
