# 用户交互补全信息手册

代码化 Dify 工作流时，DSL 永远缺三类信息：**凭据、外部资源内容、部署决策**。本手册规定何时问、问什么、怎么问。原则：**批量提问（一轮问完同阶段问题），给默认值，给推荐项**——不要挤牙膏式追问。

## 目录

- 阶段 0：获取 DSL 文件
- 阶段 1：分析后提问（缺失信息清单 → 问题）
- 阶段 2：生成前确认（技术栈与部署）
- 提问话术模板
- 用户不答时的降级策略

## 阶段 0：获取 DSL 文件

第一个问题永远是文件位置：

> 请提供 Dify 导出的 DSL 文件（.yml/.yaml）在当前机器上的完整路径。
> 如果还没导出：Dify 控制台 → 应用 → 编排页右上角「导出 DSL」。

拿到路径后先验证：文件存在 → 是 YAML → 含 `workflow.graph.nodes`。三者任一失败，立即反馈原因并请用户重新提供，不要猜。

## 阶段 1：分析后提问（缺失信息清单 → 问题）

运行 `scripts/analyze_dsl.py` 后，按 `external_requirements` 逐类生成问题：

| 分析结果字段 | 触发条件 | 问什么 | 默认/推荐 |
|---|---|---|---|
| `model_providers` | 非空 | 每个 provider 的 API Key 与 base_url（自建/代理网关？） | 推荐写入 `.env`，不直接贴在对话里 |
| `knowledge_datasets` | 非空 | **检索方案二选一**：(a) 生成项目内自建向量检索（需提供语料文件/目录）；(b) 保留调用 Dify API（需提供 Dify base_url + API Key） | 语料可获取时推荐 (a)，彻底脱离 Dify |
| `tools` | 非空 | 每个工具：保留（需提供凭据）/ 用开源实现替代 / 删除该分支 | 有标准协议（如天气、搜索）的推荐开源替代 |
| `http_endpoints` | 含 `{{#env.#}}` 或内网地址 | 实际 base URL、鉴权方式与 token | 写 `.env.example` 占位 |
| `environment_variables` | `has_value: false` | 逐项索要值；`value_type: secret` 的提示敏感 | 允许用户回复"占位即可，部署时我自己填" |
| `secret_variable_refs` | 非空 | 同上，合并提问 | 同上 |
| `plugin_dependencies` | 非空 | 对应插件的功能在代码里如何替代（SDK 直调最常见） | LLM 类插件 → 官方 SDK |
| `flags.javascript_code_nodes` | 非空 | JS 代码节点：项目引入 Node 运行时执行，还是授权改写为 Python | Python 栈时推荐授权改写 |
| `flags.file_input_variables` / `file_upload_enabled` | 非空 / true | 文件输入以什么形式传给服务（本地路径 / base64 / 对象存储 URL） | 默认本地路径 |
| `flags.uses_conversation_variables` | true | 会话变量保留（需会话存储）还是降级为单轮无状态 | 无状态降级 + 声明 |
| `agent_strategies` | 非空 | Agent 策略用哪个框架复现（function-calling 循环最常见），工具集是否全保留 | 按 tools 清单逐一确认 |

**一轮问完**：把所有问题合并成一次结构化提问（可用带选项的提问工具），而不是逐条追问。

## 阶段 2：生成前确认（技术栈与部署）

代码生成前必须确认四项，一次问完：

1. **语言/框架**（推荐项放第一）：
   - Python + FastAPI（推荐，模板现成，LLM 生态最好）
   - Node.js + Express/NestJS
   - 其他（用户指定）
2. **服务形态**：一次性 HTTP API（推荐）/ SSE 流式（chatflow 默认）/ CLI 脚本
3. **依赖管理**：pip + venv（推荐）/ poetry / npm / pnpm
4. **交付物**：纯代码项目 / 代码 + Dockerfile（推荐）/ 代码 + docker-compose

## 提问话术模板

> 我已解析 DSL：`{app.name}`（{mode} 模式，{N} 个节点 / {M} 个功能块）。生成代码前需要你确认以下信息：
>
> **凭据类**（将写入 .env.example，不会硬编码）：
> 1. OpenAI API Key —— 可回复"占位"稍后自填
> 2. TICKET_API_BASE 实际地址
>
> **资源类**：
> 3. 知识库 ds-aaa-111 等 2 个 dataset 不随 DSL 导出。选 (a) 提供语料我自建向量检索，还是 (b) 项目里继续调 Dify API？
>
> **决策类**：
> 4. 技术栈：Python+FastAPI（推荐）还是 Node.js？
> 5. 需要 Dockerfile 吗？

## 用户不答时的降级策略

| 未答项 | 降级行为 |
|---|---|
| API Key / secret | `.env.example` 写 `your_xxx_key_here`，README 标注必填 |
| 知识库方案 | 默认 (a) 自建 chroma 本地向量库，语料目录留空 + 加载脚本骨架，README 说明 |
| 工具凭据 | 保留接口签名，实现体抛 `NotImplementedError` 并注释所需凭据 |
| 技术栈 | 默认 Python + FastAPI 模板 |
| 部署物 | 默认附 Dockerfile |

**红线**：降级可以，静默不行。每一处降级都要在最终交付说明里逐条列出。
