---
name: auto-model-switch
slug: auto-model-switch
version: 1.0.0
description: "自动切换模型 - 当模型token用完或限流时，自动切换到备用模型，并通知用户。支持配置多个备用模型，智能切换策略。"
changelog: "v1.0.0 初始版本：自动检测token消耗和限流，智能切换模型"
metadata:
  clawdbot:
    emoji: "🔄"
    requires:
      bins: ["node"]
    os: ["linux", "darwin", "win32"]
---

# 自动切换模型 (Auto Model Switch)

## 概述

当主模型token用完或遇到限流时，自动切换到备用模型，确保对话不中断。

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/auto-model-switch
npm install
```

### 2. 配置模型

编辑 `config.yaml`：

```yaml
models:
  - id: primary
    model: custom-maas-coding-api-cn-huabei-1-xf-yun-com/astron-code-latest
    name: "Astron Code"
    daily_limit: 10000000
    priority: 1
  
  - id: backup-1
    model: zai/glm-5
    name: "GLM-4.5"
    daily_limit: null
    priority: 2
```

### 3. 启用心跳检查

在 `HEARTBEAT.md` 中添加：

```markdown
- 检查模型状态: node ~/.openclaw/workspace/skills/auto-model-switch/heartbeat.js
```

## 命令

| 命令 | 说明 |
|------|------|
| `node auto_model_switch.js status` | 查看当前模型状态 |
| `node auto_model_switch.js switch` | 手动切换模型 |
| `node auto_model_switch.js heartbeat` | 心跳检查（自动检测和切换） |
| `node auto_model_switch.js sync` | 从网关同步token使用量 |

## 触发条件

- **警告**：Token使用 > 80%
- **切换**：Token使用 > 95% 或 API限流

## 配置说明

```yaml
models:
  - id: primary              # 模型标识
    model: model-id          # OpenClaw模型ID
    name: "显示名称"          # 友好名称
    daily_limit: 10000000    # 每日token限制（null=无限制）
    priority: 1              # 优先级（数字越小越优先）

auto_switch:
  on_limit_exceeded: true    # token用完时切换
  on_rate_limit: true        # 限流时切换
  retry_delay: 60            # 限流后重试延迟（秒）
  warning_threshold: 0.8     # 警告阈值
  critical_threshold: 0.95   # 切换阈值

notification:
  enabled: true              # 启用通知
```

## 与OpenClaw集成

设置环境变量以启用网关集成：

```bash
export OPENCLAW_GATEWAY_URL="http://localhost:3000"
export OPENCLAW_GATEWAY_TOKEN="your-token"
```

## 示例输出

```
📊 模型状态
当前：Astron Code
Token：8.5M / 10M (85%)

备用模型：
- GLM-4.5 (可用)
```

## 文件说明

```
auto-model-switch/
├── SKILL.md              # 本文件
├── config.yaml           # 模型配置
├── auto_model_switch.js  # 主脚本
├── heartbeat.js          # 心跳脚本
├── package.json          # Node.js配置
├── QUICKSTART.md         # 快速开始
└── state/                # 状态目录（自动创建）
    ├── model-switch.json # 当前状态
    └── switch-history.json # 切换历史
```

---

_🔄 让模型切换自动化，对话永不断线_
