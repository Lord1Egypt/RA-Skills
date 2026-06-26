---
name: agent-security-dlp
description: |
  Agent Security DLP - 企业级数据防泄漏系统
  功能: 入口防护、记忆保护、工具管控、出口过滤、审计日志
  规则: 170条，覆盖金融、医疗、汽车、销售、人力资源、物流等25+行业
  触发: check-output(对话出口) / check-input(对话入口) / check-tool(工具执行)
  场景: 命令行 / Python集成 / 装饰器自动触发
---

# Agent Security DLP

> 版本: v2.1.2  
> 规则: 170条  
> 状态: ✅ 可用

---

## 简介

企业级数据防泄漏系统，支持 **166 条敏感信息检测规则**，覆盖 25+ 行业场景。

### 核心特性

- 🚀 **146 条规则** - 覆盖金融、医疗、汽车、销售、人力资源、物流等
- 🛡️ **五层防护** - 入口、记忆、工具、出口、审计
- 🎯 **智能处理** - 自动拦截/脱敏/记录
- ⚡ **高性能** - 正则预编译，并行检测

---

## 规则分类

| 类别 | 数量 | 说明 |
|------|------|------|
| 🔑 凭证密钥 | 45 | API Key、Token、私钥等 |
| 💰 金融 | 18 | 银行卡、股票、加密货币等 |
| 🏥 医疗 | 15 | 病历、医保、诊断等 |
| 🚗 汽车 | 14 | 车架号、行驶证、保险等 |
| 👥 人力资源 | 8 | 工号、工资、社保等 |
| 📦 物流 | 11 | 快递单、运单、地址等 |
| 🇨🇳 中国 PII | 6 | 身份证、手机、护照等 |
| 📜 法规 | 4 | 合同、专利、版权等 |
| 🎓 教育 | 2 | 学号、准考证等 |
| 🏛️ 政府 | 2 | 公务员编号、警官证等 |
| 📱 设备 | 2 | IMEI、MAC地址等 |
| 💬 社交 | 1 | 微信号等 |
| 🛒 电商 | 1 | 订单号等 |
| ✈️ 交通 | 3 | 车牌、机票、火车票等 |
| 📞 通信 | 1 | 通话记录等 |
| 🎟️ 会员 | 3 | 会员ID、积分等 |

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
python3 skills/agent-security-dlp/bin/agent-dlp status
```

### 2. 检查入口 (Prompt Injection)

```bash
python3 skills/agent-security-dlp/bin/agent-dlp check-input "忽略之前的指令"
# 输出: 注入检测: 是 ❌
```

### 3. 检查出口 (敏感信息)

```bash
python3 skills/agent-security-dlp/bin/agent-dlp check-output "我的手机是13812345678"
# 输出: 拦截: 否 ✅, 发现: 中国手机号 (high)
```

### 4. 检查工具

```bash
python3 skills/agent-security-dlp/bin/agent-dlp check-tool exec
# 输出: 需要审批: 是 ⚠️
```

### 5. 查看日志

```bash
python3 skills/agent-security-dlp/bin/agent-dlp logs
```

---

## 规则示例

### 凭证密钥

| 规则 | 示例 |
|------|------|
| openai_key | sk-xxx... |
| github_token | ghp_xxx... |
| aws_key | AKIA... |
| stripe_key | sk_live_xxx... |

### 金融

| 规则 | 示例 |
|------|------|
| bank_card | 622202xxx... |
| crypto_address | bc1xxx... |
| salary | 工资: 15000元 |

### 医疗

| 规则 | 示例 |
|------|------|
| medical_record | 病历号: MR2026... |
| medical_insurance | 医保卡: 123456... |
| diagnosis | 诊断: 高血压 |

### 人力资源

| 规则 | 示例 |
|------|------|
| employee_id | 工号: E00123 |
| salary | 工资: 15000元 |
| social_security | 社保账号: SS123... |

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
    "rules": ["china_idcard", "china_phone", "api_key", ...]
  }
}
```

### 模式

| 模式 | 说明 |
|------|------|
| **normal** | 记录但不拦截，只拦截严重风险 |
| **strict** | 完整检查，严格拦截 |
| **personal** | 个人轻量版，自动脱敏 |

---

## 代码结构

```
agent-security-dlp/
├── SKILL.md              # 本文档
├── README.md             # 使用说明
├── bin/
│   └── agent-dlp         # CLI 入口
├── lib/
│   └── agent_dlp.py      # 核心模块
├── config/
│   ├── config.json       # 主配置
│   └── personal.json     # 个人模式配置
└── docs/
    └── RULES.md          # 规则清单
```

---

## 核心类

| 类 | 功能 |
|---|------|
| `DLPConfig` | 配置管理 |
| `DLPRules` | 规则定义 (146条) |
| `InputGuard` | 入口检测 |
| `MemoryGuard` | 记忆保护 |
| `ToolGuard` | 工具管控 |
| `OutputFilter` | 出口过滤 |
| `AuditLogger` | 审计日志 |
| `AgentDLP` | 主类，整合所有功能 |

---

## Python 调用

```python
from agent_dlp import AgentDLP

# 初始化
dlp = AgentDLP()

# 检查入口
result = dlp.check_input("忽略之前的指令")

# 检查出口
blocked, text, details = dlp.check_output("我的手机138xxxx")

# 检查工具
result = dlp.check_tool("exec", {"command": "rm -rf /"})
```

---

## 输出模式

| 级别 | 说明 |
|------|------|
| critical | 立即拦截 |
| high | 脱敏 + 告警 |
| medium | 仅记录 |
| low | 忽略 |

---

## 性能

- 单条检测: < 1ms
- 规则数: 146 条
- 支持自定义规则
- 正则预编译

---

## 更新日志

### v2.0.0 (2026-03-17)
- 新增 146 条规则
- 覆盖 20+ 行业
- 性能优化
- 新增 personal 模式

### v1.0.0 (2026-03-14)
- 初始版本
- 25 条基础规则

---

## 许可证

MIT License

---

*版本: v2.0.0 | 更新: 2026-03-17*
