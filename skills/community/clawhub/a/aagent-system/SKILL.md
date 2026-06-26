---
name: aagent-system
description: "多智能体自动化系统，用于AI Agent技能样本采集、安全扫描、威胁情报收集和研究分析。支持单机多进程架构，可自动采集样本、检测恶意技能、提取IOC、更新规则。触发命令: /aagent start"
---

# AAgent System

多智能体自动化系统 - 技能安全研究利器

## 功能

1. **样本采集** - 从npm/GitHub/ClawHub自动采集技能样本
2. **安全扫描** - 检测恶意代码、凭证泄露、C2连接
3. **威胁情报** - 自动收集安全威胁情报
4. **规则迭代** - 持续优化检测规则

## 架构

```
采集层(4进程) → 分析层(2进程) → 研究层(2进程)
```

## 使用

### 启动系统
```
/aagent start
```

### 停止系统
```
/aagent stop
```

### 查看状态
```
/aagent status
```

### 查看样本
```
/aagent samples
```

## 管理命令

```bash
# 启动
node ~/.openclaw/workspace/skills/aagent-system/bin/agent-manager.cjs start

# 状态
node ~/.openclaw/workspace/skills/aagent-system/bin/agent-manager.cjs status

# 停止
node ~/.openclaw/workspace/skills/aagent-system/bin/agent-manager.cjs stop
```

## 配置

目标样本: 2,000,000
