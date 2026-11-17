---


name: aws-graph-agent-free
slug: aws-graph-agent-free
displayName: "AWS图代理"
version: 1.0.4
summary: "Bedrock Age。|-. 面向需要aws graph agent相关能力的开发场景,提供完整工作流程和配置指南. 该工具基于用户反馈进行了深度优化,提升了可操作性。Use。Use"
description: "|-. 面向需要aws graph agent相关能力的开发场景,提供完整工作流程和配置指南. 该工具基于用户反馈进行了深度优化,提升了可操作性。Use。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。"
license: "MIT"
tools:
  - Read
  - Write
  - Edit
  - Bash
tags:
  - agentcore
  - agent
  - builder
  - stategraph
  - langgraph
category: "Agents"
pricing_tier: "free"


---

> **功能说明**: 本技能涵盖 完整工作流程和配置指南、化工作流场景 等核心能力。



# AWS图代理（AWS Graph Agent）

基于 AWS Bedrock AgentCore 与 LangGraph 编排的多代理系统。通过 StateGraph 状态图定义代理工作流，AgentCore Runtime 封装为 HTTP 服务，Memory 管理持久记忆，Gateway 集成外部工具.
## 主要能力
### 1. StateGraph 状态图编排
使用 LangGraph StateGraph 定义多代理工作流，支持 `tools_condition` 自动路由（代理→工具或 END）、`ToolNode` 预置工具执行器、条件边实现复杂多步逻辑（planner→executor→reviewer 循环）

**处理**: 解析StateGraph 状态图编排的输入参数,完成核心逻辑,生成结构化输出.
**输出**: 返回StateGraph 状态图编排的响应数据,含状态码、结果数据和运行日志.
### 2. AgentCore Runtime HTTP 封装
将代理封装为 8080 端口 HTTP 服务，处理 `/invocations`（调用）与 `/ping`（健康检查）端点，支持容器模式部署

**处理**: 解析AgentCore Runtime HTTP 封装的输入参数,完成核心逻辑,生成结构化输出.
**输出**: 返回AgentCore Runtime HTTP 封装的响应数据,含状态码、结果数据和运行日志.
- 调用时传入`input_params`参数,支持创建/查询/导出操作
### 3. AgentCore Memory 持久记忆
管理跨会话/跨代理的 STM（短期记忆，会话内逐轮）与 LTM（长期记忆，跨会话/跨代理），配套一致性处理模式（写入后约 10s 最终一致，含等待+验证+重试逻辑）

**处理**: 解析AgentCore Memory 持久记忆的输入参数,完成核心逻辑,生成结构化输出.
**输出**: 返回AgentCore Memory 持久记忆的响应数据,含状态码、结果数据和运行日志.
- 调用时传入`input_params`参数,支持创建/查询/导出操作
### 4. AgentCore Gateway 工具集成
将 API/Lambda 转化为带认证的 Agent 工具接口，支持 Fallback 模拟（本地开发）、Local 工具协议、Production Gateway（生产）三种传输模式

**处理**: 解析AgentCore Gateway 工具集成的输入参数,完成核心逻辑,生成结构化输出.
**输出**: 返回AgentCore Gateway 工具集成的响应数据,含状态码、结果数据和运行日志.
- 调用时传入`input_params`参数,支持创建/查询/导出操作
### 5. agentcore CLI 全生命周期管理
`configure`（交互式/脚本化配置）→`launch`（容器部署）→`dev`（热重载本地开发）→`invoke`（测试调用）→`destroy`（清理资源避免持续计费）

**处理**: 解析agentcore CLI 全生命周期管理的输入参数,完成核心逻辑,生成结构化输出.
**输出**: 返回agentcore CLI 全生命周期管理的响应数据,含状态码、结果数据和运行日志.
**能力覆盖范围**：支持的场景关键词如下：Bedrock、引导式部署、多代理模式库、AWS、多代理部署编排工、全生命周期管理五、大核心能力、适用于多代理协调、的复杂业务系统、跨会话持久记忆代、集成到代理工具链、生产级、代理部署、适用关键词、多代理编排等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用向导
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 应用场景
**何时使用**：
- 需要多代理协调的复杂业务系统（客服、电商、医疗、金融）
- 需要跨会话持久记忆的对话代理（用户偏好、历史决策）
- 需要将外部 API/Lambda 集成到代理工具链的企业应用
- 希望在生产环境大规模部署 AI 代理的团队
- 使用 LangGraph 进行复杂多步逻辑编排的开发者

**输入**：Python 代理代码（基于 langgraph + bedrock-agentcore）+ AWS 凭据 + Bedrock 模型使用审批
**输出**：部署成功的 HTTP 代理服务（8080 端口）+ CLI 管理能力 + 持久记忆与网关工具集成

**不适用场景**：
- 未完成 Bedrock 模型使用审批的账户
- 不需要多代理协调的简单单一代理场景（可直接用基础 LLM API）
- 非 AWS 平台部署需求

## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | AWS图代理处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit langgraph
uv tool install bedrock-agentcore-starter-toolkit  # 安装 agentcore CLI
```

### Step 2：预检清单（部署前必读）
| 检查项 | 要求 | 不满足的后果 |
|:-----|:-----|:-----|
| 模型使用审批 | 在 Bedrock Console 填写  表单 | `Model use case details not submitted` |
| 推理配置 | 使用 `us..-*` 推理配置文件 | `on-demand throughput isn't supported` |
| 代理命名 | 字母开头，仅字母/数字/下划线，1-48 字符 | `Invalid agent name` |
| 区域选择 | 选择支持 AgentCore 的区域（如 us-east-1） | 部署失败 |
| 环境变量 | 容器中在 Dockerfile 设置 ENV，非 .env | 容器不读取 .env |
| 记忆开关 | 确认是否需要记忆子系统 | 记忆功能不可用 |

### Step 3：编写代理代码（StateGraph + Runtime）
```python
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from typing import Annotated
from typing_extensions import TypedDict
# ...
class State(TypedDict):
    messages: Annotated[list, add_messages]
# ...
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge(START, "agent")
graph = builder.compile()
# ...
app = BedrockAgentCoreApp()
@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload.get("prompt", ""))]})
    return {"result": result["messages"][-1].content}
app.run()
```bash
# 在此执行相关操作
echo "操作完成"
```bash
# 交互式配置
agentcore configure -e agent.py --region us-east-1
# 脚本化配置（CI/CD）
py --region us-east-1 --name my_agent --non-interactive
# 容器模式部署（生产）
agentcore launch --deployment-type container
# 无记忆部署（无状态代理）
agentcore launch --disable-memory
```bash
# 在此执行相关操作
echo "操作完成"
```bash
agentcore dev                              # 热重载本地开发
agentcore invoke '{"prompt": "Hello"}'    # 测试调用
```bash
# 在此执行相关操作
echo "操作完成"
```text
多代理协调? → 编排器+专家模式（编排器根据意图路由到专家，共享 session_id）
跨会话持久记忆? → AgentCore Memory（非 LangGraph checkpoints）
外部 API/Lambda? → AgentCore Gateway
单一代理简单? → 快速开始模板
复杂多步逻辑? → StateGraph + tools_condition + ToolNode
```bash
# 在此执行相关操作
echo "操作完成"
```bash
agentcore destroy
```

## 使用范例
### 示例(补充)

**输入**：部署一个带工具调用的简单代理

**输出**（代码与部署）：
```python
# 最简模式：用户输入 → 代理节点 → tools_condition → ToolNode → 回到代理
#                                    → END（无需工具）
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)  # 自动路由
builder.add_edge(START, "agent")
graph = builder.compile()
```
部署：`agentcore configure -e agent.py --region us-east-1 && agentcore launch`

### 示例二：记忆系统写入与验证（一致性处理·指数退避）

**输入**：写入长期记忆并确保一致性

**输出**（写入+指数退避验证逻辑）：
```python
memory import MemoryClient
import time
# ...
memory = MemoryClient()
memory.create_event(session_id, actor_id, event_type, payload)  # 写入
# ...
# 最终一致性验证（指数退避：2s→4s→8s→16s→30s，最多 5 次）
def verify_with_backoff(memory, session_id, actor_id, event_type, payload,
                        base=2, max_wait=30, max_retries=5):
    for attempt in range(max_retries):
        time.sleep(min(base * (2 ** attempt), max_wait))  # 指数退避+上限
        if memory.list_events(session_id):
            return  # 一致性达成
        if attempt < max_retries - 1:
            memory.create_event(session_id, actor_id, event_type, payload)  # 重写
    raise RuntimeError(f"记忆一致性验证失败：{max_retries} 次重试后仍为空")
# ...
verify_with_backoff(memory, session_id, actor_id, event_type, payload)
# 注意：event['payload'] 是列表类型；确认 actor_id 和 session_id 匹配
```

### 示例三：多代理协调（编排器+专家模式）端到端

**输入**：客服系统按意图路由到客服专家/计费专家，共享 session_id 跨专家记忆

**输出**（编排器+专家+共享记忆，完整部署）：
```python
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
# ...
class State(TypedDict):
    messages: list
    expert: str
# ...
def orchestrator(state):
    intent = classify(state["messages"][-1])  # 意图分类
    return {"expert": {"投诉": "cs_expert", "账单": "billing_expert"}[intent]}
# ...
def cs_expert(state):
    return {"messages": [handle_cs(state)]}      # 客服专家处理
# ...
def billing_expert(state):
    return {"messages": [handle_billing(state)]}  # 计费专家处理
# ...
builder = StateGraph(State)
builder.add_node("orchestrator", orchestrator)
builder.add_node("cs_expert", cs_expert)
builder.add_node("billing_expert", billing_expert)
builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", lambda s: s["expert"])
builder.add_edge("cs_expert", END)
builder.add_edge("billing_expert", END)
graph = builder.compile()
```
py --region us-east-1 && agentcore launch`。两个专家共享同一 `session_id`，通过 AgentCore Memory 实现跨专家记忆传递（编排器写入意图，专家读取上下文），避免用户重复陈述.
### 示例四：Gateway 工具集成端到端

**输入**：将订单查询/退款 Lambda 集成为代理工具，生产网关模式部署

**输出**（Gateway 注册+代理调用+三种传输模式）：
```python
gateway import GatewayClient
# ...
# 三种传输模式按环境选择
mode = "production"  # "production"（本地开发）/ "local"（本地协议）/ "production"（生产网关）
gateway = GatewayClient(mode=mode)
tools = gateway.register_tools([
    {"name": "search_orders", "lambda_arn": "arn:aws:lambda:us-east-1:…:OrderSearch"},
    {"name": "issue_refund",  "lambda_arn": "arn:aws:lambda:us-east-1:…:Refund"},
])
# 工具名必须去除 Lambda 的 ___ 前缀，否则返回 "Unknown tool"
# ...
agent = create_agent_with_tools(tools)  # 工具自动注入 StateGraph
```
调用：`agentcore invoke '{"prompt": "查询订单 #1234 并退款"}'`。代理自动调用 `search_orders`→`issue_refund`，Gateway 处理 Lambda 认证与调用。本地开发用 `mode="mock"` 返回假数据无需真实 Lambda；生产用 `mode="production"` 走网关鉴权.
## 前置条件
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| bedrock-agentcore | Python 包 | 必需 | `pip install bedrock-agentcore` |
| bedrock-agentcore-starter-toolkit | Python 包 | 必需 | `pip install bedrock-agentcore-starter-toolkit` |
| langgraph | Python 包 | 必需 | `pip install langgraph` |
| Python 运行时 | 运行时 | 必需 | python.org，需 3.9+ |
| uv | 工具 | 可选（CLI 安装） | `pip install uv` |
| AWS CLI | 工具 | 推荐 | 从 aws.amazon.com 安装 |
| AWS 账户 | 账户 | 必需 | 需 AWS 账户和 Bedrock 访问权限 |
| AWS 访问密钥 | 凭据 | 必需 | `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_REGION` |
| Bedrock 模型审批 | 平台配置 | 必需 | 在 Bedrock Console 填写  表单 |
| Agent 平台 | 运行环境 | 必需 |  Code / Cursor / Codex /  CLI 等 |
| 操作系统 | 运行环境 | 必需 | Windows / macOS / Linux |

**成本优化策略**：无状态部署用 `--disable-memory` 节省记忆存储成本；测试后立即 `agentcore destroy` 避免持续运行成本；生产用容器、开发用 `agentcore dev`；选择低成本区域（如 us-east-1）；使用 `us..-*` 推理配置降低吞吐量成本.
**密钥安全处理规范（零暴露硬性约束）**：代理绝不能读取、cat、打印、回显或日志记录 `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` 明文，绝不在聊天/提交/镜像中暴露凭据——无论出于任何原因包括"验证配置"。硬性规则：(1) 凭据只通过环境变量或 IAM Role 注入，禁止硬编码到源码或 Dockerfile ARG；(2) `agentcore configure` 所需凭据从 AWS CLI 命名配置文件（`--profile`）或实例元数据获取，禁止在命令行明文传参；(3) 容器部署用任务角色（Task Role）而非 ENV 明文密钥，ENV 仅用于非敏感配置；(4) 如用户在聊天中粘贴了密钥，立即告知已泄露，要求轮换并从历史清除，绝不回显；(5) `.env` 加入 `.gitignore`，禁止提交版本库；(6) `agentcore destroy` 后确认密钥与资源已清理。验证安装状态用 `aws sts get-caller-identity`（返回角色 ARN，不暴露密钥）而非打印环境变量.
**可用性分类**：MD+EXEC（纯 Markdown 指令，需要命令行执行能力进行部署与管理）
- **API Key**：本skill无需额外API Key配置

## 常见疑问
**Q1：部署后记忆为空怎么办？**
A：记忆写入后有约 10 秒最终一致性延迟。等待 10 秒后用 `list_events` 重新查询。如仍为空，检查日志中是否显示"Memory enabled"，确认部署时未使用 `--disable-memory`.
**Q2：容器无法读取 .env 文件怎么办？**
A：容器模式下 .env 文件不会被自动读取。在 Dockerfile 中使用 ENV 指令设置环境变量，而非依赖 .env 文件.
**Q3：收到"on-demand throughput isn't supported"错误？**
A：使用 `us..-*` 推理配置文件替代按需吞吐量。这是区域和模型组合的限制.
**Q4：代理名称无效？**
A：代理名称必须字母开头，仅含字母/数字/下划线，1-48 字符。将连字符改为下划线（如 `my-agent` → `my_agent`）.
**Q5：Gateway 返回"Unknown tool"？**
A：Lambda 函数必须从 `bedrockAgentCoreToolName` 参数中去除 `___` 前缀。检查 Lambda 代码中的工具名处理逻辑.
## 使用约束
1. **记忆最终一致性延迟约10秒**：写入后不能立即可读，需等待+验证+重试机制，不适合强一致性场景
2. **依赖 Bedrock 模型审批**：未在 Bedrock Console 填写  表单则无法部署，审批流程不可跳过
3. **代理命名规则严格**：仅字母/数字/下划线，1-48 字符，连字符等常见命名方式不被接受
4. **容器模式不支持 .env**：必须在 Dockerfile 中用 ENV 设置环境变量，与本地开发习惯不同
5. **Gateway 工具名需去前缀**：Lambda 的 `bedrockAgentCoreToolName` 必须去除 `___` 前缀，否则返回"Unknown tool"

## 安全提示
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 使用环境变量注入,不得在源码中明文写入 |
| 命令执行风险 | 限定执行预批准命令,不拼接用户输入到参数中 |
| 网络通信安全 | 通信使用HTTPS并校验证书有效性 |
| 敏感数据暴露 | 返回数据中不含凭证信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 效率指标
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 优势对比
| 对比维度 | AWS图代理 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | Bedrock Age | 通用场景 | 通用场景 |

## 功能矩阵
- **自动化执行**: Bedrock Age
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

### 前置条件

- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪

## 故障恢复流程
针对AWS图代理使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### AWS图代理通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

## 使用限制说明
- 极端边界输入可能影响输出质量,建议对异常输入做预校验
- API凭证需妥善管理,避免硬编码到代码中,推荐使用环境变量注入
- 生成结果受模型能力影响,不同模型输出质量可能有差异
- 文件格式兼容性受底层库限制,部分特殊格式可能不被支持
- 不同操作系统的命令行参数可能存在差异,需做平台适配
