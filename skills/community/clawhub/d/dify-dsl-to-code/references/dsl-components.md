# Dify 工作流/对话流组件全书

代码化 Dify 应用时的案头参考：每个组件（节点）的用途、DSL 属性、输出变量与代码化要点。属性名均取自真实导出的 DSL（见 `assets/examples/`），而非凭记忆。

## 目录

- 一、应用模式与 DSL 顶层结构
- 二、图结构：节点、边、迭代子图
- 三、变量系统
- 四、组件详表
  - 开始 start ｜ 结束 end ｜ 直接回复 answer
  - LLM ｜ 问题分类器 ｜ 知识检索 ｜ Agent
  - 条件分支 if-else ｜ 迭代 iteration ｜ 循环 loop
  - 代码执行 ｜ 模板转换 ｜ 变量聚合器 ｜ 变量赋值 ｜ 参数提取器 ｜ 文档提取器 ｜ 列表操作
  - HTTP 请求 ｜ 工具 tool
- 五、代码化速查表

---

## 一、应用模式与 DSL 顶层结构

`app.mode` 决定语义，代码化前先看它：

| mode | 名称 | 收尾节点 | 特点 |
|---|---|---|---|
| `workflow` | 工作流 | `end` | 单轮自动化，批处理场景 |
| `advanced-chat` | 对话流 Chatflow | `answer`（可多个、可在中间流式输出） | 多轮对话，带记忆/会话历史 |
| `chat` / `agent-chat` / `completion` | 基础聊天/Agent/文本生成 | 无 graph | **不导出 workflow 图**，本 skill 不适用 |

DSL 顶层字段：

```yaml
app: {name, mode, description, icon, icon_background}
kind: app
version: 0.3.0            # 0.1.x 无 dependencies；0.3.x 有插件市场依赖
workflow:
  graph: {nodes: [...], edges: [...], viewport: {...}}
  environment_variables: [{id, name, value, value_type}]   # value_type: string|number|secret
  conversation_variables: [{id, name, value_type, value}]  # 会话级持久变量（chatflow）
  features: {file_upload, opening_statement, suggested_questions, ...}
dependencies: [{type: marketplace, value: {marketplace_plugin_unique_identifier: "langgenius/openai_api_compatible:0.0.12@hash..."}}]
```

## 二、图结构：节点、边、迭代子图

**节点**：画布层字段（`position/width/height/zIndex/type: custom`）只是渲染信息；**语义全在 `node.data`**：

```yaml
- id: '1745225236216'
  parentId: '1739938724217'      # 仅迭代内部节点有，指向所属 iteration 节点
  data:
    type: knowledge-retrieval     # ← 组件类型，唯一权威字段
    title: 知识检索
    desc: ''
    isInIteration: true           # 是否在迭代体内
    iteration_id: '1739938724217' # 所属迭代
    ...组件属性...
```

**边**：`{id, source, target, sourceHandle, targetHandle, data: {sourceType, targetType, isInIteration}}`。

- `sourceHandle: source` 普通直连；`"true"/"false"` 来自 if-else；条件 id 或分类序号来自多分支节点；`iteration-start` 的出边在迭代体内部。
- **迭代子图**：iteration 节点的内部节点平铺在 nodes 列表里，靠 `parentId`/`isInIteration` 归属；体内有一个 `type: iteration-start` 的虚拟起点（id 形如 `<迭代id>start`）。循环同理（`loop-start`）。

## 三、变量系统

| 变量类别 | 引用语法 | 代码化映射 |
|---|---|---|
| 节点输出 | `{{#node_id.var#}}` | 变量池 `(node_id, var)` |
| 系统变量 | `sys.query` `sys.files` `sys.user_id` `sys.conversation_id` `sys.dialogue_count` | 运行时注入的请求上下文 |
| 环境变量 | `{{#env.NAME#}}` | 进程环境变量 |
| 密钥 | `{{#secret.NAME#}}` | 进程环境变量，只写 .env 占位 |
| 会话变量 | conversation_variables 中的 name | 有状态存储（chatflow）；无状态可降级 |
| 上下文 | llm 节点内 `{{#context#}}` | 知识检索结果拼接文本 |

start 节点的输入变量类型：`text-input`（短文本）、`paragraph`（长文本）、`select`（下拉，带 options）、`number`、`file`（单文件）、`file-list`（文件列表）；均可设 `required`、`default`、`label`。

## 四、组件详表

### 开始 start

流程入口，无上游。属性只有 `variables[]`（见上）。输出：每个变量 + 全部 `sys.*`。代码化：生成 API 入参 schema。

### 结束 end（workflow 专用）

| 属性 | 说明 |
|---|---|
| `outputs[]` | `{variable: 输出名, value_selector: [node_id, var]}` |

代码化：组装响应体；引用被剪枝分支的变量时输出 null（与 Dify 一致）。

### 直接回复 answer（chatflow 专用）

| 属性 | 说明 |
|---|---|
| `answer` | 模板文本，支持 `{{#...#}}` 插值 |

可在流程中间多次出现实现分段流式输出。代码化：SSE 流式响应（默认）或一次性返回（问用户）。

### LLM

最重的组件，属性：

| 属性 | 说明 |
|---|---|
| `model.provider` | 如 `openai`、`langgenius/openai_api_compatible/openai_api_compatible`（市场插件形式） |
| `model.name` / `model.mode` | 模型名 / `chat` 或 `completion` |
| `model.completion_params` | `temperature`、`max_tokens`、`top_p`、`stop` 等，原样透传 |
| `prompt_template[]` | `[{role: system\|user\|assistant, text}]`，text 内含插值；chatflow 里还可能是 `{edition_type: basic\|jinja2}` |
| `context.enabled` + `context.variable_selector` | 挂接知识检索结果，prompt 内用 `{{#context#}}` |
| `vision.enabled` | 图片输入（取 `sys.files`） |
| `memory` | chatflow 专有：`{window: {enabled, size}, query_prompt_key}` 对话历史 |
| `structured_output_enabled` / `structured_output` | JSON Schema 约束输出 |
| `reasoning_format` | 思维链输出格式 |

输出变量：`text`、`reasoning_content`（思维链模型）、`usage`、`structured_output`。代码化：provider SDK + 先插值再调用 + 参数透传；**需要 API Key**。

### 问题分类器 question-classifier

| 属性 | 说明 |
|---|---|
| `query_variable_selector` | 待分类文本（常是 `[sys, query]`） |
| `classes[]` | `[{id: '1', name: 类别名}]`，id 即出边 sourceHandle |
| `model` / `instruction` | 分类用小模型 / 补充指令 |

输出：`class_id`、`class_name`。代码化：LLM 分类调用或规则映射，handler 须把选中的 class id 写入变量池供路由。

### 知识检索 knowledge-retrieval

| 属性 | 说明 |
|---|---|
| `query_variable_selector` | 检索 query |
| `dataset_ids[]` | 知识库 id 列表；**部分私有化部署会导出为加密串**，且内容不随 DSL 导出 |
| `retrieval_mode` | `single`（单库，可用 `model` 做 query 改写）/ `multiple`（多库） |
| `multiple_retrieval_config` | `{top_k, score_threshold, reranking_enable, reranking_model}` |

输出：`result`（分段数组）。代码化：自建向量检索（需语料）或回调 Dify API——**必须问用户**，见 interaction-playbook。

### Agent

`agent_strategy`（function-calling / ReAct 等市场插件策略）、`agent_parameters`、`model`、`tools[]`。代码化：function-calling 循环 + 工具注册表。

### 条件分支 if-else

| 属性 | 说明 |
|---|---|
| `conditions[]` | `{id, variable_selector, comparison_operator, value}` |
| `logical_operator` | `and` / `or` |
| `cases[]` | **新版结构**：多 case 分支 `[{case_id, logical_operator, conditions}]`，出边 handle 为 case_id；旧版只有 true/false |

comparison_operator 全集：`contains`、`not contains`、`start with`、`end with`、`is`、`is not`、`empty`、`not empty`、`=`、`≠`、`>`、`<`、`≥`、`≤`、`null`、`not null`、`exists`、`not exists`、`in`、`not in`、`all of`、`length =/></≥/≤`。代码化：注意字符串/数字比较的类型转换。

### 迭代 iteration

| 属性 | 说明 |
|---|---|
| `iterator_selector` | 待遍历的数组变量 |
| `output_selector` | 体内哪个节点的输出聚合成结果数组 |
| `output_type` | 输出类型（通常 `array[string]`） |
| `is_parallel` / `parallel_nums` | 并行迭代（新版） |

体内子图见「图结构」。输出：聚合数组。代码化：for/map；并行版用线程池，注意视觉/LLM 类调用并发上限。

### 循环 loop

`loop_variables[]`（循环内可变的变量）、`break_conditions`（退出条件，同 if-else 条件结构）、`loop_count`（最大次数兜底）。代码化：while + 条件求值 + 计数上限。

### 代码执行 code

| 属性 | 说明 |
|---|---|
| `code_language` | `python3` / `javascript` |
| `code` | **内联完整源码**，Dify 沙箱约定 `main(arg1, ...) -> dict` |
| `variables[]` / `inputs` | 入参映射：`{variable: 形参名, value_selector: [...]}` |
| `outputs` | 出参声明：`{key: {type, children}}` |

代码化铁律：**原样搬运，禁止重写逻辑**；javascript 代码需 Node 运行时或征得用户同意后改写。

### 模板转换 template-transform

`template`：Jinja2 模板（`{{ var }}` 语法，注意与 Dify 变量插值 `{{#...#}}` 是两层）；`variables[]` 入参映射。输出：`output`。零 token 成本，能用它就别用 LLM。

### 变量聚合器 variable-aggregator

`variables[]`：多路 `[node_id, var]` 选择器；`output_type`；`advanced_settings.group_enabled` + `groups[]`（分组聚合）。语义：取第一路非 None 的值。用于 if-else 多分支汇合。

### 变量赋值 variable-assigner

`items[]`：`{input_variable_selector: [会话变量], value: [来源选择器]}`。写入 conversation_variables，跨轮次保存。代码化：需会话存储；无状态服务降级为上下文变量并声明。

### 参数提取器 parameter-extractor

`model`、`query`、`parameters[]`（`{name, type, description, required}`）、`instruction`、`reasoning_mode`（prompt/function_call）。用 LLM 从自然语言抽结构化参数，供后置工具/HTTP 使用。

### 文档提取器 document-extractor

`variable_selector`（file/file-list 变量）、`is_array_file`。按类型解析 PDF/DOCX/TXT/PPT/XLSX 为文本。代码化：pypdf / python-docx 等按 MIME 分派。

### 列表操作 list-operator

`item_selector`（数组变量）、`filter_conditions`（按属性过滤/排序/取前 N）。代码化：数组 filter/sort/slice。

### HTTP 请求 http-request

| 属性 | 说明 |
|---|---|
| `method` | get/post/put/patch/delete/head |
| `url` | 支持插值；常含 `{{#env.X#}}` |
| `params` / `headers` | 字符串键值对（`k:v` 换行分隔） |
| `body` | `{type: none\|form-data\|x-www-form-urlencoded\|raw-text\|json\|binary, data}` |
| `authorization` | `{type: no-auth\|api-key, config: {type: basic\|bearer\|custom, header, value}}` |
| `timeout` | `{connect, read, write}` 秒 |
| `ssl_verify` | 是否校验证书 |

输出：`status_code`、`body`、`headers`、`files`。代码化：httpx/requests，先插值再请求；鉴权 token 进 .env。

### 工具 tool

`provider_id`、`provider_type`（builtin/marketplace/api/workflow）、`tool_name`、`tool_configurations`（工具级配置）、`tool_parameters`（LLM 填充的参数声明）。凭据不随 DSL 导出。代码化三选一问用户：保留（要凭据）/ 开源实现替代 / 删除该分支。

## 五、代码化速查表

| 组件 | 生成代码落点 | 常见缺失信息 |
|---|---|---|
| start/end/answer | definition.py + main.py（answer 由引擎流式收集，SSE 走 /run/stream） | 无 |
| llm | services/llm.py + blocks/ | provider API Key、base_url |
| 问题分类器 | runner 内置路由 + blocks/ 分类 handler | 同上 |
| 知识检索 | services/retrieval.py | **语料来源或 Dify API 凭据** |
| if-else（含 cases[]）/loop/iteration | runner 引擎内置（并行迭代降级为顺序，需声明） | 无 |
| code | blocks/ 原样封装 | 无 |
| http-request | services/http.py | base URL、token |
| tool | services/tools.py | 插件凭据、替代方案 |
| 变量赋值 | 会话存储层 | 是否接受无状态降级 |

> 节点 → 代码的映射策略另见 [dsl-node-types.md](dsl-node-types.md)；缺失信息如何问用户见 [interaction-playbook.md](interaction-playbook.md)。
