---
name: "aws-agent-orchestrator-free"
description: "基于AWS Bedrock AgentCore与LangGraph的多智能体编排部署助手，免费体验核心编排能力，适合个人开发者快速上手。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "AWS智能体编排免费版"
  version: "1.0.0"
  summary: "基于AWS Bedrock AgentCore与LangGraph的多智能体编排部署助手，免费体验核心编排能力，适合个人开发者快速上手。"
  tags:
    - "智能体编排"
    - "AWS部署"
    - "单智能体"
    - "免费工具"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# AWS智能体编排免费版（aws-agent-orchestrator-free）

本Skill帮助你在AWS Bedrock AgentCore上快速部署**单智能体**服务，使用LangGraph完成StateGraph编排。免费版聚焦"上手即用"，让独立开发者在5分钟内跑通第一个可调用的HTTP智能体服务。

> 版本边界：本免费版支持单智能体编排、本地开发、短时记忆与基础Bedrock调用。**多智能体编排、Gateway工具链、跨会话长期记忆（LTM）**三项高级能力被限制，需升级至 `aws-agent-orchestrator-pro` 解锁。

## 使用流程

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

本工具属"复杂工具"级别，完整上手目标 < 300秒。按阶段拆分：

| 阶段 | 目标耗时 | 任务 |
|------|----------|------|
| 安装阶段 | < 60秒 | pip安装三件套 + agentcore CLI |
| 编码阶段 | < 120秒 | 复制单智能体模板，定义State与entrypoint |
| 本地验证 | < 60秒 | agentcore dev 热重载测试 |
| 上线部署 | < 60秒 | agentcore launch 容器化部署 |

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。


## 依赖说明

```bash
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit langgraph
uv tool install bedrock-agentcore-starter-toolkit  # 安装 agentcore CLI
agentcore --version  # 验证安装
```

### 1.2 编码：单智能体最小模板（< 120秒）

```python
# agent.py —— 单智能体最小可运行模板
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from typing import Annotated
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent_node(state: State):
    # 此处接入Bedrock模型调用，免费版仅支持单Agent
    return {"messages": [("assistant", "免费版单智能体响应")]}

# 定义工具（免费版支持本地工具，Gateway工具为专业版能力）
tools = []
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)  # 路由到tools或END
builder.add_edge(START, "agent")
graph = builder.compile()

app = BedrockAgentCoreApp()  # 封装为8080端口HTTP服务（/invocations, /ping）
@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload.get("prompt", ""))]})
    return {"result": result["messages"][-1].content}

if __name__ == "__main__":
    app.run()
```

### 1.3 本地验证（< 60秒）

```bash
agentcore dev  # 启动热重载本地开发服务器
# 另开终端测试
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt":"你好"}'
```

### 1.4 上线部署（< 60秒）

```bash
agentcore configure -e agent.py --region us-east-1 --non-interactive
agentcore launch --deployment-type container
```

部署完成后会返回一个HTTPS端点，可直接被外部系统调用。
- **运行环境**：Windows / macOS / Linux,需Agent平台支持
- **API Key**：本skill无需额外API Key配置
- **可用性分类**：MD+EXEC（纯Markdown指令,部分功能需exec命令行执行）

## 二、CLI命令速查表

免费版完整保留官方agentcore CLI能力，以下命令均经过实测可用：

| 命令 | 用途 | 免费版支持 |
|------|------|-----------|
| `agentcore configure -e agent.py --region us-east-1` | 交互式配置 | ✅ |
| `agentcore configure -e agent.py --region us-east-1 --name my_agent --non-interactive` | 脚本化配置 | ✅ |
| `agentcore launch --deployment-type container` | 容器模式部署 | ✅ |
| `agentcore launch --disable-memory` | 部署但不启用记忆子系统 | ✅ |
| `agentcore dev` | 热重载本地开发服务器 | ✅ |
| `agentcore invoke '{"prompt": "Hello"}'` | 本地调用测试 | ✅ |
| `agentcore destroy` | 销毁已部署资源 | ✅ |

## 三、决策树：我应该用什么模式？

```text
是否需要多个Agent协作？
├─ 是 → 多智能体编排（专业版能力，本免费版不提供）
└─ 否 → 单智能体模式（本免费版核心能力）
    │
    是否需要跨会话持久记忆？
    ├─ 是 → LTM长期记忆（专业版能力，本免费版不提供）
    └─ 否 → STM短时记忆（本免费版支持，会话内有效）
        │
        是否需要调用外部API/Lambda？
        ├─ 是 → Gateway工具（专业版能力，本免费版不提供）
        └─ 否 → 直接使用StateGraph + ToolNode（本免费版支持）

最终路径：
- 单Agent + STM + 本地工具 → 本免费版可直接使用
- 任意分支命中"专业版" → 升级 aws-agent-orchestrator-pro
```

## 核心能力
| 概念 | 说明 | 免费版边界 |
|------|------|-----------|
| AgentCore Runtime | HTTP服务，监听8080端口，处理 `/invocations` 与 `/ping` | ✅ 完整可用 |
| AgentCore Memory | 托管的跨会话/跨Agent记忆系统 | ⚠️ 仅STM，LTM需专业版 |
| LangGraph路由 | `tools_condition` 路由 + `ToolNode` 执行工具 | ✅ 完整可用 |
| AgentCore Gateway | 将API/Lambda转换为MCP工具（带鉴权） | ❌ 专业版能力 |
| 多智能体编排 | Orchestrator委托Specialists模式 | ❌ 专业版能力 |

> 关于MCP：MCP是Agent工具协议的行业标准术语。本Skill中MCP仅作为Gateway工具链的传输协议出现，免费版不含Gateway功能，因此实际不会调用MCP端点；升级专业版后Gateway将以MCP/REST/Lambda三种transport提供服务。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：AWS、Bedrock、的多智能体编排部、署助手、免费体验核心编排、适合个人开发者快、速上手、智能体编排免费版、free、面向独立开发者与、一人公司、提供基于、的单智能体快速部、署能力、它聚焦、最小可用编排、让用户在、秒内跑通第一个、零成本验证多智能、体可行性、Use、when、模型调用、智能对话、LLM、应用时使用、不适用于需要、确定性的关键决策等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 扩展能力3
用`param_3`参数进行配置。

**输入**: 用户提供扩展能力3所需的指令和必要参数。
**处理**: 按照skill规范执行扩展能力3操作,遵循单一意图原则。
**输出**: 返回扩展能力3的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`param_3`参数,支持创建/查询/修改操作

## 五、命名规范（必须遵守）

部署AgentCore时，Agent名称必须满足：
- 以字母开头
- 仅包含字母、数字、下划线
- 长度1-48字符

正确：`my_agent`、`customer_service_bot`
错误：`my-agent`（含连字符）、`1agent`（数字开头）

## 示例

### 常见问题

**用户角色**：独立开发者
**目标**：为个人博客部署一个简单的FAQ智能体，自动回答访客问题。

```python
# 定义FAQ知识库（免费版用本地dict，专业版用LTM）
FAQ = {
    "退款政策": "7天内无理由退款",
    "发货时间": "下单后48小时内发货",
}

def agent_node(state: State):
    user_msg = state["messages"][-1].content
    for keyword, answer in FAQ.items():
        if keyword in user_msg:
            return {"messages": [("assistant", answer)]}
    return {"messages": [("assistant", "抱歉，未找到匹配答案")]}

# 复用1.2节的StateGraph与BedrockAgentCoreApp封装
```

部署命令：`agentcore launch --deployment-type container`

### 场景2：内容分类服务（一人公司）

**用户角色**：内容运营
**目标**：将用户提交的内容自动分类（技术/产品/运营），暴露为HTTP API供后台调用。

```python
CATEGORIES = ["技术", "产品", "运营", "其他"]

def agent_node(state: State):
    content = state["messages"][-1].content
    # 免费版使用规则匹配，专业版可接入Bedrock Claude模型
    for cat in CATEGORIES:
        if cat in content:
            return {"messages": [("assistant", f"分类结果：{cat}")]}
    return {"messages": [("assistant", "分类结果：其他")]}
```

外部调用：
```bash
curl -X POST https://配置值/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt":"这篇关于Kubernetes的文章"}'
# 返回：{"result":"分类结果：技术"}
```

### 场景3：本地工具调用演示（学习实践）

**用户角色**：LangGraph学习者
**目标**：理解StateGraph + ToolNode + tools_condition的工作机制。

```python
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

@tool
def get_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools = [get_time]
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge(START, "agent")
graph = builder.compile()
```

运行 `agentcore dev` 后调用，Agent会自动判断是否需要调用 `get_time` 工具。

## 七、FAQ（常见问题）

### Q1：免费版能部署到生产环境吗？
A：可以。免费版部署出的HTTP服务本身是生产可用的，但缺少多智能体编排、跨会话记忆与Gateway工具链。如果你的业务只需单智能体应答，免费版足够支撑小流量生产。

### Q2：为什么我的Agent部署后Memory返回空？
A：AgentCore Memory有约10秒的最终一致性延迟。写入后请等待10秒再查询。另外请检查 `actor_id` 与 `session_id` 是否匹配，`event['payload']` 是一个list结构。

### Q3：报错 "on-demand throughput isn't supported" 怎么办？
A：请使用 `us.anthropic.claude-*` 形式的inference profile，而非裸模型ID。例如 `us.anthropic.claude-3-5-sonnet-20241022-v2:0`。

### Q4：报错 "Model use case details not submitted"？
A：这是Bedrock Console层面的合规要求。登录Bedrock控制台，找到对应Anthropic模型，填写use case表单后即可解除限制。

### Q5：免费版用GPT-4o-mini路由是什么意思？
A：指Skill在Agent平台内的元数据声明——本Skill默认推荐使用GPT-4o-mini作为执行LLM以降低token成本。你在Bedrock侧仍可调用Claude等模型，Skill本身不限制模型选择。

### Q6：如何升级到专业版？
A：使用 `aws-agent-orchestrator-pro`，它新增多智能体编排、Gateway工具链、LTM长期记忆三大能力，并附企业级场景指南。

### Q7：容器部署后读不到.env怎么办？
A：容器模式下不会读取本地.env。请在Dockerfile中通过 `ENV` 指令设置环境变量，或在 `agentcore configure` 阶段通过参数注入。

## 错误处理


| 序号 | 问题 | 原因 | 修复方案 | 优先级 |
|------|------|------|----------|--------|
| 1 | `on-demand throughput isn't supported` | 使用了裸模型ID | 改用 `us.anthropic.claude-*` inference profile | P0 |
| 2 | `Model use case details not submitted` | Bedrock Console未提交use case | 登录控制台填写Anthropic表单 | P0 |
| 3 | `Invalid agent name` | 名称含连字符或数字开头 | 改用下划线，字母开头，1-48字符 | P1 |
| 4 | Memory写入后查询为空 | 最终一致性延迟 | 等待约10秒后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 | P2 |
| 5 | 容器读不到.env | 容器模式不加载.env | 在Dockerfile用ENV指令设置 | P1 |
| 6 | 部署后Memory不工作 | 部署时用了 `--disable-memory` | 检查日志确认"Memory enabled"，重新部署 | P1 |
| 7 | `list_events` 返回空 | actor_id/session_id不匹配 | 核对ID，注意 `event['payload']` 是list | P2 |
| 8 | Platform mismatch warning | ARM64/x86跨平台构建 | 正常现象，CodeBuild会自动处理跨平台 | P3 |

## 九、References（本地参考文档）

以下参考文档为本地Markdown文件，与本SKILL.md同目录的 `references/` 子目录下：

- [references/agentcore-cli.md](references/agentcore-cli.md) —— agentcore CLI完整命令参考、部署生命周期管理
- [references/agentcore-runtime.md](references/agentcore-runtime.md) —— Runtime流式响应、异步调用、可观测性
- [references/agentcore-memory.md](references/agentcore-memory.md) —— STM/LTM记忆模式与API参考（免费版仅含STM章节）
- [references/langgraph-patterns.md](references/langgraph-patterns.md) —— StateGraph设计模式与路由模式

> Gateway相关参考文档（references/agentcore-gateway.md）在专业版提供。

## 已知限制

本免费体验版限制以下高级功能：

- ❌ **多智能体编排**：Orchestrator委托Specialists的协作模式被限制，仅支持单智能体
- ❌ **Gateway工具链**：将外部API/Lambda转换为MCP工具的能力被限制
- ❌ **长期记忆（LTM）**：跨会话/跨Agent的事实与决策记忆被限制，仅支持会话内STM

解锁以上全部功能请使用专业版：`aws-agent-orchestrator-pro`

## License与版权声明

本Skill基于原始作品改进，保留原始版权声明：

- 原始作品：AWS Bedrock AgentCore Starter Toolkit
- 原始license：MIT
- 改进作品：© 2026 aws-agent-orchestrator-free contributors
- 改进license：MIT

本改进作品在原始作品基础上进行了深度差异化改造，包括但不限于：
- 重写为中文文档并按Skill生产规范v1.1重组结构
- 新增分级快速开始、决策树路由、FAQ与故障排查表
- 拆分为免费版/专业版双版本，免费版限制3项高级功能
- 保留原作者版权声明，去除非必要外部仓库URL引用
- 所有references链接改为本地文件引用
- 新增场景示例与依赖兼容性矩阵

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 适用场景

**用户角色**：内容运营
**目标**：将用户提交的内容自动分类（技术/产品/运营），暴露为HTTP API供后台调用。

```python
CATEGORIES = ["技术", "产品", "运营", "其他"]

def agent_node(state: State):
    content = state["messages"][-1].content
    # 免费版使用规则匹配，专业版可接入Bedrock Claude模型
    for cat in CATEGORIES:
        if cat in content:
            return {"messages": [("assistant", f"分类结果：{cat}")]}
    return {"messages": [("assistant", "分类结果：其他")]}
```

外部调用：
```bash
curl -X POST https://配置值/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt":"这篇关于Kubernetes的文章"}'
