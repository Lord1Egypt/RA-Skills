---
name: agent-dlp
description: |
  Agent DLP - 数据防泄漏系统
  功能: 入口防护、记忆保护、工具管控、出口过滤、审计日志
  触发: (1)检查状态 (2)检查输入 (3)检查输出
---

# Agent DLP - 数据防泄漏系统

> 版本: v1.0.0  
> 状态: ✅ 可用

---

## 功能

| 功能 | 说明 |
|------|------|
| **Input Guard** | 入口防护，检测 Prompt Injection |
| **Memory Guard** | 记忆保护，检测污染和敏感信息 |
| **Tool Guard** | 工具管控，危险工具审批 |
| **Output Filter** | 出口过滤，敏感信息脱敏/拦截 |
| **Audit Logger** | 审计日志，记录所有操作 |

---

## 架构

```
用户输入 → Input Guard → Agent → Memory Guard → Tool Guard → Output Filter → 用户
              注入检测        记忆检查      工具审批      脱敏拦截
                    ↓                                    ↓
              审计日志                              审计日志
```

---

## 使用方式

### 1. 查看状态

```bash
python3 lib/agent_dlp.py status

# 或
python3 bin/agent-dlp status
```

### 2. 检查入口 (Prompt Injection)

```bash
python3 bin/agent-dlp check-input "忽略之前的指令"
# 输出: 注入检测: 是 ❌
```

### 3. 检查出口 (敏感信息)

```bash
python3 bin/agent-dlp check-output "我的手机是13812345678"
# 输出: 拦截: 否 ✅, 发现: 中国手机号 (high)
```

### 4. 检查工具

```bash
python3 bin/agent-dlp check-tool exec
# 输出: 需要审批: 是 ⚠️
```

### 5. 查看日志

```bash
python3 bin/agent-dlp logs
```

---

## 规则

### 敏感信息规则

| 规则 | 类型 | 动作 |
|------|------|------|
| china_idcard | 身份证 | 拦截 |
| china_phone | 手机号 | 脱敏 |
| api_key | API Key | 拦截 |
| aws_key | AWS Key | 拦截 |
| private_key | 私钥 | 拦截 |
| credit_card | 信用卡 | 拦截 |
| password | 密码 | 脱敏 |
| email | 邮箱 | 脱敏 |

### 注入检测模式

| 模式 | 示例 |
|------|------|
| ignore_previous | "忽略之前的指令" |
| role_override | "你现在是另一个AI" |
| privilege_escalation | "admin mode override" |

---

## 配置

编辑 `config/config.json`:

```json
{
  "enabled": true,
  "mode": "normal",
  "input": {
    "injection_detection": true
  },
  "output": {
    "enabled": true,
    "rules": ["china_idcard", "china_phone", "api_key"]
  }
}
```

### 模式

| 模式 | 说明 |
|------|------|
| **normal** | 记录但不拦截，只拦截严重风险 |
| **strict** | 完整检查，严格拦截 |

---

## 代码结构

```
agent-dlp/
├── SKILL.md           # 本文档
├── bin/
│   └── agent-dlp      # CLI 入口
├── lib/
│   └── agent_dlp.py   # 核心模块
├── config/
│   └── config.json    # 配置文件
└── logs/              # 审计日志
```

---

## 核心类

| 类 | 功能 |
|---|------|
| `DLPConfig` | 配置管理 |
| `DLPRules` | 规则定义 |
| `InputGuard` | 入口检测 |
| `MemoryGuard` | 记忆保护 |
| `ToolGuard` | 工具管控 |
| `OutputFilter` | 出口过滤 |
| `AuditLogger` | 审计日志 |
| `AgentDLP` | 主类，整合所有功能 |

---

## 示例

### Python 调用

```python
from agent_dlp import AgentDLP

# 初始化
dlp = AgentDLP()

# 检查入口
result = dlp.check_input("忽略之前的指令")

# 检查出口
blocked, text, details = dlp.check_output("我的手机13812345678")

# 检查工具
result = dlp.check_tool("exec", {"command": "rm -rf /"})
```

---

*版本: v1.0.0 | 创建日期: 2026-03-14*
