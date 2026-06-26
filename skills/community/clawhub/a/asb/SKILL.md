---
name: asb
description: Agent Service Bus - 智能服务编排和协作平台，通过 MCP Server 集成所有 ASB 能力
version: 0.2.0
license: MIT-0
author: ASB Team
tags: [asb, service-bus, orchestration, mcp, agent]
metadata:
  openclaw:
    requires:
      bins:
        - uv
      anyBins:
        - python3
        - python
    install:
      - kind: uv
        package: agent-service-bus
    homepage: https://github.com/qiyueqiu/Agent-Service-Bus
    emoji: "🚌"
---

# ASB - Agent Service Bus

ASB 是将传统 ESB 升级为包含 AI Agent 服务的智能消息总线。通过 MCP Server，所有 ASB 能力都可以在 Claude Desktop 中直接使用。

## 快速开始

### 在 Claude Desktop 中使用

在 Claude Desktop 配置文件中添加：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "asb": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/Agent-Service-Bus",
        "run",
        "asb",
        "mcp",
        "serve",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

重启 Claude Desktop 后即可使用。

## 可用能力

### 核心 ASB 能力

| Tool | 描述 |
|------|------|
| `asb-service-discovery` | 发现和查询可用服务 |
| `asb-service-composition` | 服务组合和智能编排 |
| `asb-governance` | 治理和监控能力 |

### 通用工具

| Tool | 描述 |
|------|------|
| `orchestration` | 智能任务编排 |
| `service-discovery` | 服务发现 |
| `llm-provider` | LLM 调用 |
| `echo` | 回显测试 |
| `calculator` | 基础计算 |
| `message-send` | 消息发送 |

## 使用示例

```
User: 帮我找一下可用的数据分析服务

Claude: [调用 asb-service-discovery]
找到以下数据分析服务:
- data-processor v1.0.0
- analytics-engine v2.1.0

User: 用 analytics-engine 分析销售数据

Claude: [调用 orchestration Skill]
正在执行智能编排...
```

## 其他集成方式

### A2A Agent 协作

ASB 也支持 A2A (Agent-to-Agent) 协议：

```python
# 获取 ASB AgentCard
agent_card = await discover_agent("asb-agent")

# 查看可用能力
capabilities = agent_card.capabilities
```

### CLI 命令行

安装 ASB CLI 后：

```bash
# 列出所有 Skills
asb skills list

# 智能编排
asb orchestrate "分析销售数据并生成报告"

# 服务发现
asb discover services
```

## 安装 ASB

```bash
# 克隆仓库
git clone https://github.com/qiyueqiu/Agent-Service-Bus.git
cd Agent-Service-Bus

# 使用 uv 安装
uv sync
```

## 更多信息

- GitHub: https://github.com/qiyueqiu/Agent-Service-Bus
- 文档: https://github.com/qiyueqiu/Agent-Service-Bus/tree/main/docs
