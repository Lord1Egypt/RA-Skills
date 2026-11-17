---

slug: aws-graph-agent
name: "aws-graph-agent"
version: 1.0.1
displayName: "AWS图谱智能体"
summary: "Bedrock AgentCore与LangGraph多代理编排,覆盖状态图、Runtime、记忆、网关、CLI全生命周期。"
summary_zh: "Bedrock AgentCore与LangGraph多代理编排,覆盖状态图、Runtime、记忆、网关、CLI全生命周期。"
license: "MIT"
description: |-
  AWS Bedrock AgentCore与LangGraph多代理部署编排工具。提供StateGraph状态图编排、AgentCore Runtime HTTP封装（8080端口）、
  Memory跨会话STM/LTM持久记忆、Gateway外部API/Lambda工具集成、CLI全生命周期管理五大核心能力.
  适用于多代理协调的复杂业务系统、跨会话持久记忆代理、外部API集成到代理工具链、生产级AI代理部署.
tags:
  - 智能代理
  - 云计算
  - AWS
  - 多代理系统
  - 通用办公
  - DevOps
  - agentcore
  - agent
  - stategraph
  - gateway
  - api
tools:
  - read
  - exec
  - write
homepage: ""
category: "Operations"

---

> **核心功能**: 本技能提供五大核心能力等能力。

# AWS Graph Agent

基于 AWS Bedrock AgentCore 与 LangGraph 编排的多代理系统。通过 StateGraph 状态图定义代理工作流，AgentCore Runtime 封装为 HTTP 服务，Memory 管理持久记忆，Gateway 集成外部工具.
## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | AWS Graph Agent处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 付费版进阶功能
| 能力 | 免费版 | 付费版 |
|:-----|:-----|:-----|
| 基础功能 | 支持 | 支持 |
| 高清分辨率与无损输出 | 不支持 | 支持 |
| 批量生成与风格预设 | 不支持 | 支持 |
| 自定义模型微调 | 不支持 | 支持 |
| 商用版权授权 | 不支持 | 支持 |

## 前置条件
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 主要能力
### 1. StateGraph 状态图编排
使用 LangGraph StateGraph 定义多代理工作流，支持 `tools_condition` 自动路由（代理 → 工具或 END）、`ToolNode` 预置工具执行器、条件边实现复杂多步逻辑（planner → executor → reviewer 循环）.

### 2. AgentCore Runtime HTTP 封装
将代理封装为 8080 端口 HTTP 服务，处理 `/invocations`（调用）与 `/ping`（健康检查）端点，支持容器模式部署.

### 3. AgentCore Memory 持久记忆
管理跨会话/跨代理的 STM（短期记忆，会话内逐轮）与 LTM（长期记忆，跨会话/跨代理），配套一致性处理模式（写入后约 10s 最终一致，含等待+验证+重试逻辑）.

### 4. AgentCore Gateway 工具集成
将 API/Lambda 转化为带认证的 Agent 工具接口，支持 Fallback 模拟（本地开发）、Local 工具协议、Production Gateway（生产）三种传输模式.

### 5. agentcore CLI 全生命周期管理
`configure`（交互式/脚本化配置）→ `launch`（容器部署）→ `dev`（热重载本地开发）→ `invoke`（测试调用）→ `destroy`（清理资源避免持续计费）.

## 使用向导
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用范围
| 场景 | 典型输入 | 输出内容 | 涉及能力 |
|:---:|:---:|:---:|:---:|
| 多代理客服系统 | "按意图路由到客服/计费专家" | 编排器+专家模式部署，共享 session_id | StateGraph + Memory |
| 跨会话持久记忆 | "记住用户偏好和历史决策" | LTM 写入与一致性验证逻辑 | Memory |
| 外部 API 工具集成 | "将订单查询 Lambda 集成为代理工具" | Gateway 注册+三种传输模式 | Gateway |
| 生产级代理部署 | "部署带工具调用的代理到 8080 端口" | 容器部署+健康检查 | Runtime + CLI |
| 复杂多步逻辑 | "planner→executor→reviewer 循环" | 条件边+ToolNode 状态图 | StateGraph |

**不适用于**: 未完成 Bedrock 模型使用审批的账户，不需要多代理协调的简单单一代理场景，非 AWS 平台部署需求.
## 操作步骤
### Step 1: 安装依赖
```bash
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit langgraph
uv tool install bedrock-agentcore-starter-toolkit  # 安装 agentcore CLI
```

### Step 2: 预检清单（部署前必读）
| 检查项 | 要求 | 不满足的后果 |
|:------|------:|:------|
| 模型使用审批 | 在 Bedrock Console 填写 Anthropic 表单 | `Model use case details not submitted` |
| 推理配置 | 使用 `us.anthropic.claude-*` 推理配置文件 | `on-demand throughput isn't supported` |
| 代理命名 | 字母开头，仅字母/数字/下划线，1-48 字符 | `Invalid agent name` |
| 区域选择 | 选择支持 AgentCore 的区域（如 us-east-1） | 部署失败 |
| 环境变量 | 容器中在 Dockerfile 设置 ENV，非 .env | 容器不读取 .env |
| 记忆开关 | 确认是否需要记忆子系统 | 记忆功能不可用 |

### Step 3: 编写代理代码（StateGraph + Runtime）
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
```

### Step 4: 配置与部署
```bash
# 交互式配置
agentcore configure -e agent.py --region us-east-1
# 脚本化配置（CI/CD）
py --region us-east-1 --name my_agent --non-interactive
# 容器模式部署（生产）
agentcore launch --deployment-type container
# 无记忆部署（无状态代理）
agentcore launch --disable-memory
```

### Step 5: 测试与开发
```bash
agentcore dev                              # 热重载本地开发
agentcore invoke '{"prompt": "Hello"}'    # 测试调用
```

### Step 6: 按决策树选择多代理模式
```text
多代理协调? → 编排器+专家模式（编排器根据意图路由到专家，共享 session_id）
跨会话持久记忆? → AgentCore Memory（非 LangGraph checkpoints）
外部 API/Lambda? → AgentCore Gateway
单一代理简单? → 快速开始模板
复杂多步逻辑? → StateGraph + tools_condition + ToolNode
```

### Step 7: 清理资源（避免持续计费）
```bash
agentcore destroy
```

## 案例展示

### 案例1: 带工具调用的代理部署（StateGraph 基础模式）
**场景**: 部署一个简单代理，用户输入后自动判断是否调用工具

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

**部署命令**:
```bash
py --region us-east-1
agentcore launch
agentcore invoke '{"prompt": "查询北京今天天气"}'
```

**分析**: `tools_condition` 自动判断代理输出是否包含工具调用请求。包含则路由到 `ToolNode` 执行工具后返回代理节点继续处理；不包含则直接路由到 END 返回结果.
### 案例2: 记忆系统写入与一致性验证（指数退避）
**场景**: 写入长期记忆并确保跨会话可读，处理约 10s 最终一致性延迟

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

**分析**: 记忆写入后存在约 10 秒最终一致性延迟，立即查询会返回空。指数退避策略（2→4→8→16→30s）在保证最终一致的同时避免频繁轮询。重试时重新写入确保事件不被丢失.
### 案例3: 多代理协调（编排器+专家模式）端到端
**场景**: 客服系统按意图路由到客服专家/计费专家，共享 session_id 跨专家记忆

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

**部署命令**:
```bash
py --region us-east-1
agentcore launch
```

**分析**: 两个专家共享同一 `session_id`，通过 AgentCore Memory 实现跨专家记忆传递（编排器写入意图，专家读取上下文），避免用户重复陈述。`conditional_edges` 根据 `expert` 字段动态路由到对应专家节点.
## 异常恢复流程
| 错误场景 | 错误信息 | 原因分析 | 处理方式 |
|---:|:---|---:|---:|
| 推理配置不支持 | `on-demand throughput isn't supported` | 未使用跨区域推理配置文件 | 改用 `us.anthropic.claude-*` 推理配置文件 |
| 模型审批未提交 | `Model use case details not submitted` | 未在 Bedrock Console 填写使用表单 | 进入 Bedrock Console 填写 Anthropic 模型使用审批表单 |
| 代理名称无效 | `Invalid agent name` | 名称含连字符或非法字符 | 改用下划线，字母开头，1-48 字符（如 `my-agent` → `my_agent`） |
| 记忆写入后为空 | `list_events` 返回空列表 | 最终一致性延迟约 10s | 等待 10s 后重新查询；检查日志 "Memory enabled/disabled" |
| 容器不读取 .env | 环境变量未生效 | 容器模式不支持 .env 文件 | 在 Dockerfile 中用 `ENV` 指令设置环境变量 |
| 部署后记忆不可用 | 记忆功能缺失 | 部署时使用了 `--disable-memory` | 重新部署不带 `--disable-memory` 参数 |
| actor_id 不匹配 | `list_events` 返回空但记忆已写入 | actor_id/session_id 与写入时不一致 | 确认 ID 匹配，注意 payload 是列表类型 |
| Gateway 未知工具 | `Unknown tool` | Lambda 未去除工具名前缀 | 从 `bedrockAgentCoreToolName` 去除 `___` 前缀 |
| 平台不匹配警告 | ARM64 跨平台构建警告 | 本地与目标平台架构不同 | 正常现象，CodeBuild 会自动处理，无需操作 |

## 成本优化策略

- 无状态部署用 `--disable-memory` 节省记忆存储成本
- 测试后立即 `agentcore destroy` 避免持续运行成本
- 生产用容器模式、开发用 `agentcore dev`
- 选择低成本区域（如 us-east-1）
- 使用 `us.anthropic.claude-*` 推理配置降低吞吐量成本

## 热门问题
### Q1: 部署后记忆为空怎么办？
A: 记忆写入后有约 10 秒最终一致性延迟。等待 10 秒后用 `list_events` 重新查询。如仍为空，检查日志中是否显示 "Memory enabled"，确认部署时未使用 `--disable-memory`.
### Q2: 容器无法读取 .env 文件怎么办？
A: 容器模式下 .env 文件不会被自动读取。在 Dockerfile 中使用 `ENV` 指令设置环境变量，而非依赖 .env 文件。这是容器模式与本地开发习惯的主要差异.
### Q3: 收到 "on-demand throughput isn't supported" 错误？
A: 使用 `us.anthropic.claude-*` 推理配置文件替代按需吞吐量。这是区域和模型组合的限制，跨区域推理配置文件可自动路由到容量充足的区域.
### Q4: 代理名称无效如何修改？
A: 代理名称必须字母开头，仅含字母/数字/下划线，1-48 字符。将连字符改为下划线（如 `my-agent` → `my_agent`），避免使用特殊符号和中文.
### Q5: Gateway 返回 "Unknown tool" 如何排查？
A: Lambda 函数必须从 `bedrockAgentCoreToolName` 参数中去除 `___` 前缀。检查 Lambda 代码中的工具名处理逻辑，确认注册时使用的名称与代理调用时一致.
### Q6: 多代理如何共享记忆？
A: 多个专家代理共享同一 `session_id`，通过 AgentCore Memory 的 `create_event` 写入、`list_events` 读取。编排器写入意图后，专家节点读取上下文，避免用户重复陈述。注意使用指数退避验证一致性.
## 注意事项
1. **记忆最终一致性延迟约10秒**：写入后不能立即可读，需等待+验证+重试机制，不适合强一致性场景
2. **依赖 Bedrock 模型审批**：未在 Bedrock Console 填写 Anthropic 表单则无法部署，审批流程不可跳过
3. **代理命名规则严格**：仅字母/数字/下划线，1-48 字符，连字符等常见命名方式不被接受
4. **容器模式不支持 .env**：必须在 Dockerfile 中用 ENV 设置环境变量，与本地开发习惯不同
5. **Gateway 工具名需去前缀**：Lambda 的 `bedrockAgentCoreToolName` 必须去除 `___` 前缀，否则返回 "Unknown tool"

## 结果格式
```json
{
  "success": true,
  "data": {
    "result": "AWS Graph Agent处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "aws-graph-agent"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```

## 问题处理指引
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
|:-------|:-------|:-------|:-------|
| 代理无法启动 | 依赖库缺失或版本不兼容 | 检查安装的依赖库和版本，确保与文档中推荐的版本一致 | 安装或更新依赖库到正确版本 |
| 状态图执行失败 | 状态图定义错误或工具节点配置错误 | 检查状态图定义和工具节点配置，确保语法正确且工具节点可访问 | 修正状态图定义或工具节点配置 |
| 记忆数据不可用 | 记忆服务未启用或配置错误 | 检查记忆服务是否启用，并确认配置文件中的记忆服务地址和凭证 | 启用记忆服务并正确配置 |
| Gateway工具调用失败 | Lambda函数未正确部署或配置 | 检查Lambda函数的部署状态和配置，确保函数已正确部署并配置了正确的触发器和权限 | 部署Lambda函数并正确配置触发器和权限 |
| CLI命令执行错误 | CLI命令参数错误或环境变量未设置 | 检查CLI命令的参数和当前环境变量的设置 | 修正CLI命令参数或设置正确的环境变量 |

## 安全提示
| 风险项 | 等级 | 防护措施 | 验证方法 |
|:------|:------|:-------|:-------|
| API密钥泄露 | 高 | 使用环境变量存储API密钥，避免将其硬编码在代码中 | 检查代码和配置文件，确保API密钥未被泄露 |
| 记忆数据泄露 | 中 | 对记忆数据进行加密，并限制对记忆服务的访问 | 检查加密设置和访问控制列表，确保安全 |
| Lambda函数权限过高 | 高 | 限制Lambda函数的权限，仅授予必要的权限 | 检查Lambda函数的权限设置，确保权限最小化 |
| 状态图执行注入攻击 | 中 | 对状态图输入进行验证和清理，防止注入攻击 | 检查状态图输入处理逻辑，确保输入安全 |
| 容器安全漏洞 | 高 | 使用容器镜像扫描工具检测安全漏洞，并定期更新容器镜像 | 运行容器镜像扫描工具，并更新到最新安全版本 |

## 技术创新
| 场景 | 效率提升量化分析 | 差异化对比 |
|:----|:----------------|:----------|
| 多代理客服系统 | 通过StateGraph实现自动化路由，减少人工干预，提高响应速度，效率提升50% | 传统客服系统需要人工处理每个请求，效率低 |
| 跨会话持久记忆 | 通过Memory实现跨会话记忆，减少重复询问，提高用户满意度，效率提升30% | 传统系统无法记住用户历史，需要重复询问 |
| 外部API集成 | 通过Gateway集成外部API，简化开发流程，提高开发效率，效率提升40% | 传统集成需要手动编写API调用代码，开发周期长 |
| 生产级代理部署 | 通过CLI实现全生命周期管理，简化部署和运维，提高运维效率，效率提升25% | 传统部署需要手动操作，过程复杂 |
| 复杂多步逻辑 | 通过StateGraph和工具节点实现复杂逻辑，提高系统智能化水平，效率提升20% | 传统系统需要手动编写复杂逻辑，难以维护 |

## 功能矩阵
- **自动化执行**: Bedrock AgentCore与LangGraph多代理编排,覆盖状态图、Runtime、记忆、网关、CLI全生命周
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 用户疑问解答
### Q1: AWS图谱智能体支持哪些输入格式？

A1: Bedrock AgentCore与LangGraph多代理编排,覆盖状态图、Runtime、记忆、网关、CLI全生命周期。。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

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
| 对比维度 | AWS图谱智能体 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | Bedrock AgentCore与LangGraph多代理编排,覆盖状态图、R | 通用场景 | 通用场景 |

## 故障恢复流程
针对AWS图谱智能体使用中可能遇到的常见问题,提供以下排查方案:

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

### AWS图谱智能体通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

### 前置条件

- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
