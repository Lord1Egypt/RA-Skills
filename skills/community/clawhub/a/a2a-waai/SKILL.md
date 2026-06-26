---
name: a2a
description: "Agent Interconnect - Discover and invoke other AI Agents. Use when: need cross-platform collaboration, delegate tasks to specialized agents, or build multi-agent systems. / Agent互联互通 - 发现并调用其他AI Agent。"
metadata: 
  author: "WaaiOn"
  version: "1.1"
  openclaw: 
    emoji: "🔗"
    requires: 
      bins: ["python3"]
---

# 🔗 A2A - Agent Interconnect / Agent 互联互通

Enable OpenClaw to collaborate with other AI Agents through standard protocol.

## When to Use / 使用场景

| EN | CN |
|----|----|
| Need to call other AI agents | 需要调用其他AI Agent |
| Build multi-agent system | 构建多Agent系统 |
| Delegate complex tasks | 委托复杂任务给专业Agent |
| Cross-platform collaboration | 跨平台协作 |

## Design / 设计原则

| EN | CN |
|----|----|
| Concise: 6 fields only | 简洁: 仅6字段 |
| Elegant: Decorator registration | 优雅: 装饰器注册 |
| High-performance: Connection pool | 高性能: 连接池复用 |

## Message Types / 消息类型

| Type | EN | CN | Scenario |
|------|----|----|----------|
| call | Synchronous call | 同步调用 | Need result immediately |
| cast | Notification | 通知 | No response needed |
| task | Async task | 异步任务 | Time-consuming operations |

## Core API / 核心API

```python
from a2a import Server, Client, Registry

# Server / 服务端
s = Server('my_agent')
@s.action('echo')
async def echo(p): return p

# Client / 客户端  
c = Client('caller')
r = await c.call('ws://host:8766', 'action', {})

# Registry / 注册中心
r = Registry()
r.reg(Agent('id','name','ws://ep',{'cap':'rw'}))
agents = r.find('cap')
```

## Examples / 示例

```bash
# Discover agents that can draw
发现能画图的Agent

# Delegate task
Ask Coze to draw a panda / 让Coze帮我画一只熊猫
```

## Installation / 安装

```bash
npx clawhub install a2a-waai
```

## Author / 作者

- WaaiOn
