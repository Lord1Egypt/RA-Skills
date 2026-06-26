# dimens-manager 工作流章节 能力状态矩阵

本文档用于回答一个核心问题：当前工作流能力中，哪些已由 `dimens-cli` 封装，哪些仍是 `server-only`，哪些属于“部分对齐但需额外说明”。

## 1. 能力状态总览

| 能力域 | 典型能力 | 当前状态 | 说明 |
| --- | --- | --- | --- |
| OpenAI 兼容聊天调用 | `POST /app/flow/:teamId/v1/chat/completions` | 已封装 | CLI 已提供 `dimens-cli ai chat-completions` |
| 团队工作流管理 | 列表、详情、创建、发布、草稿管理 | server-only | 当前 Skill 可解释，但 CLI 未全面收口成稳定命令 |
| 项目工作流挂载 | 查询绑定、挂载、解绑、入口开关 | server-only | 项目可见性问题不能只靠 chat 接口判断 |
| 工作流运行执行 | `run/invoke`, `run/debug` | server-only（部分命令别名可能存在） | 排查时要区分“调试链路”和“正式执行链路” |
| 默认模型配置读取 | `flow_config(type=default_models)` | 部分对齐 | 文档定义清晰，但不同链路生效范围不同 |
| 节点模型自动回退 | LLM 节点缺省模型回退 | 部分对齐（未完全统一） | `chat/completions` 默认模型模式已通，普通节点不应默认假设自动回退 |
| AI 生成审批工作流草案 | 业务蓝图、`pluginType=approval` 图 JSON、落地计划 | Skill 已覆盖 | 可通过 `dimens-cli ai chat-completions` 辅助产出草案 |
| 项目内审批工作流创建 / 更新 / 发布 | `/app/approval/:teamId/:projectId/workflow/create|update|publish` | 已有项目路由 | 这是项目内直接创建链路，创建后即归属项目；CLI 未必已完整封装 |
| 团队安装实例 / 项目绑定 | `flow_info`、项目工作流绑定、`systemView=approval` | server-only | 适用于团队复用、跨项目挂载、安装实例和入口绑定判断 |

## 2. 推荐表达模板

当用户问“这个能力现在能不能直接用 CLI 做”时，建议固定按下面模板回答：

1. 先给能力状态：`已封装 / server-only / 部分对齐`。
2. 再给调用建议：优先 CLI 还是需要走服务端接口。
3. 最后给风险边界：是否受 `teamId/projectId/systemView/model` 影响。

示例表达：

- “`chat/completions` 已封装，建议优先走 `dimens-cli ai chat-completions`。”
- “项目挂载查询目前仍是 server-only，需要结合项目绑定关系排查，不要只看聊天调用。”
- “默认模型在聊天兼容链路已可用，但工作流普通 LLM 节点是否自动回退仍需按当前实现确认。”
- “审批工作流 AI 生成已由 Skill 覆盖为草案生成能力；项目内创建有独立路由，团队安装实例和项目绑定仍需结合服务端接口或产品界面。”

## 3. 与 `examples.md` 的分工

- `examples.md` 负责“接口级案例总览”。
- 本文档负责“能力是否已封装、可否直接 CLI 调用、边界在哪里”。

这样可以避免 `examples.md` 同时承担规则解释和能力分级。
