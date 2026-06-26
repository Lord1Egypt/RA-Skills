# Agent OS

## 描述
基于三层架构的AI智能体操作系统模板 - 身份层/操作层/知识层分离

## 功能
- 提供可复用的AI智能体三层架构模板
- 身份层定义"我是谁"
- 操作层定义"如何工作"
- 知识层积累"学到了什么"

## 用法
```bash
cd ~/agent-os
./scripts/startup.sh    # 启动系统
./scripts/verify.sh     # 验证架构
```

## 架构
```
identity/      # 第一层：身份层
  SOUL.md      # 核心灵魂
  IDENTITY.md  # 角色配置
  USER.md      # 用户画像

operations/    # 第二层：操作层
  AGENTS.md    # 代理团队
  HEARTBEAT.md # 系统心跳
  ROLE-CEO.md  # 角色指南

knowledge/     # 第三层：知识层
  MEMORY.md    # 长期记忆
  shared-context/  # 跨会话状态
```

## 标签
agent, architecture, template, ai-system

## 版本
1.0.0
