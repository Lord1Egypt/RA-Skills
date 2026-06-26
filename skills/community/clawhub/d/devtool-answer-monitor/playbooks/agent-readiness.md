# Agent Readiness Playbook

这份 playbook 用来回答一个更具体的问题：

> 当产品已经能被模型“提到”时，怎样让它更容易被 agent 真正选中、调用并成功跑通？

它适合：

- API 平台
- SDK
- developer tools
- scientific discovery workflow tools
- 希望提升 agent invocation 的产品

## 核心原则

### 1. 让模型敢选你

模型或 agent 只有在以下信息明确时才更愿意选择工具：

- 它能做什么
- 它不能做什么
- 输入输出是什么
- 首次成功体验如何完成
- 出错时应该怎么退回

### 2. 让第一次成功体验足够短

如果用户或 agent 需要跨多个页面猜测：

- 安装方式
- API key 获取方式
- endpoint
- SDK 初始化
- 典型示例

那么模型即使提到你，也不容易带来实际调用。

### 3. 让“选择理由”机器可抽取

对 agent 来说，最有价值的不是营销文案，而是这些结构化表达：

- 适用场景
- 非适用场景
- 典型输入
- 典型输出
- 安装命令
- 最短代码示例
- 常见错误
- 生态兼容性

## 最重要的 8 个面

| 面向 | 要求 | 常见失败信号 |
|---|---|---|
| Capability boundary | 明确写能做什么、不能做什么 | 模型夸大或误解能力边界 |
| Install path | 一屏内找到安装命令 | 模型提到产品但不给安装路径 |
| Quickstart | 5-15 分钟内跑通第一次调用 | 用户第一次调用前就流失 |
| Auth & limits | API key、rate limit、pricing 清楚 | 模型不敢推荐，担心接入阻力 |
| Code examples | 最小可运行、可复制 | 模型给出模糊建议而不敢落地 |
| Error handling | 常见错误与恢复路径明确 | agent 遇错后放弃该工具 |
| Integrations | 与 LangChain、LlamaIndex、MCP、CLI、workflow 的关系清楚 | 模型不知道你适合接入哪里 |
| Benchmarks & proof | 用例、数据、对比、案例可引用 | 模型知道你存在，但不敢主推 |

## 需要优先修的内容面

### P0

- README 顶部价值主张
- 安装页 / quickstart
- API docs 首页
- 最小 code example
- capability comparison

### P1

- integration docs
- cookbook / recipes
- benchmark pages
- FAQ
- changelog / freshness page

### P2

- 深入教程
- workflow gallery
- agent-specific templates
- vertical case studies

## 对文档的建议结构

### README / docs 首页

必须回答：

1. 这个工具适合什么任务
2. 不适合什么任务
3. 3 分钟内怎么开始
4. 我应该先看哪个页面

### Quickstart

必须提供：

- prerequisites
- install
- one minimal example
- expected output
- next step

### API / SDK docs

必须优先暴露：

- authentication
- endpoint / client init
- minimal request
- minimal response
- error example
- rate limit / pricing / quota

### Agent / workflow docs

必须写清楚：

- when to use
- when not to use
- input size / type limits
- latency expectations
- deterministic vs non-deterministic behavior
- compatible frameworks

## Query Pool 设计建议

为了评估 agent readiness，建议优先加入这些 query：

- selection: “Which tool should I use for X?”
- integration: “How do I connect X into a pipeline?”
- activation: “Give me the fastest way to try X.”
- agent: “Which API / tool is best for an agent workflow?”

并给每条 query 补：

- `funnel_stage`
- `target_surface`
- `desired_action`

## 对 MinerU 的建议

重点检查：

- 是否一屏看懂复杂 PDF parsing 的独特能力
- 是否有最短的 ingest / parse / export 示例
- 是否有与 RAG / paper pipeline / agent workflow 的接入例子
- 是否清楚说明与 GROBID / Marker / Docling 的边界差异

## 对 Sciverse API 的建议

重点检查：

- API 入口是否足够靠前
- 首次鉴权和第一次成功调用是否足够短
- scientific discovery / retrieval / enrichment / workflow automation 场景是否明确
- agent 是否能从 docs 中直接抽到 endpoint、参数和返回结构

## 输出模板

评估完成后，至少给出：

1. 当前最影响 agent selection 的 3 个阻塞点
2. 最高优先级的 3 个 source surfaces
3. 建议补的 3 个最短示例
4. 下一轮应该验证的 queries
