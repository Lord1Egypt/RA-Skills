---
name: evomap-auto-maintainer
description: 自动维护 EvoMap 节点在线状态，自动赚取积分。一键设置，永久生效。
version: 1.0.0
author: zhanglingAI
price: $19.99
tags: [automation, evomap, node-management, heartbeat, passive-income]
---

# EvoMap Auto Maintainer

保持你的 EvoMap 节点 24/7 在线，自动赚取积分。

## 解决的问题

- EvoMap 节点经常离线？
- 不想手动发送心跳？
- 节点掉线后不知道怎么恢复？

这个技能帮你全自动解决！

## 功能

- ✅ **自动检测** - 每分钟检查节点状态
- ✅ **自动心跳** - 每15分钟发送保活信号
- ✅ **智能恢复** - 离线时自动重新注册获取密钥
- ✅ **日志记录** - 详细记录每次操作

## 安装

```bash
clawhub install evomap-auto-maintainer
```

## 配置

设置环境变量：

```bash
export EVOMAP_NODE_ID="node_your_node_id"
export EVOMAP_SECRET="your_node_secret"
```

## 使用

### 1. 检查节点状态
```bash
bash maintainer.sh status
```

输出示例：
```
[2026-03-08 22:50:20] 检查节点状态...
[2026-03-08 22:50:20] 节点ID: node_openclaw_xxx
[2026-03-08 22:50:22] ✅ 节点在线
```

### 2. 设置自动维护（推荐）
```bash
bash maintainer.sh setup
```

这将自动：
- 添加 cron 任务，每15分钟自动心跳
- 无需人工干预，永久生效

### 3. 手动发送心跳
```bash
bash maintainer.sh heartbeat
```

## 价格

**$19.99** - 一次性购买，永久使用，免费更新

## 收益计算

- 保持节点在线 = 赚取 EvoMap 积分
- 积分可兑换收益
- 投资回报：通常 1-2 个月回本

## 支持

如有问题请联系：zl18616313005@gmail.com
