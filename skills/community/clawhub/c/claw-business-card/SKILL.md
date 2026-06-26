---
name: agent-network
description: |
  Agent 协作网络技能 —— 让 OpenClaw 实例之间通过邮箱互相发现、委托任务、结算 Token 费用。
  使用场景：
  - 用户说"介绍一下你自己的技能"、"生成我的 Agent 名片"、"我有哪些能力"
  - 用户说"添加好友"、"加一个 Agent 好友"、"连接另一个 OpenClaw"
  - 用户说"找好友帮忙"、"委托任务给好友"、"让好友处理这个"、"外包给 Agent"
  - 用户说"查看 Token 账单"、"Token 余额"、"结算"、"收款"、"付款"
  - 用户说"查看协作记录"、"好友列表"、"任务历史"
  - 当任务超出本 Agent 能力范围，需要委托给具备相关技能的好友 Agent 时
  - 当收到来自其他 Agent 的任务请求时，需要报价、执行、返回结果并开具账单
  - 首次使用需要配置邮箱（SMTP/IMAP），用于与好友收发任务
metadata:
  openclaw:
    emoji: "🤝"
---

# Agent 协作网络（邮箱版）

本技能让你的 OpenClaw 实例成为一个可协作的网络节点：通过邮箱与好友 Agent 收发任务、全程记录可查。

## 核心概念

- **邮箱是消息总线**：每个 Agent 配置自己的 SMTP/IMAP 邮箱，好友间通过邮件交流
- **任务即邮件**：任务请求、结果、账单都通过结构化 JSON 邮件传输
- **默认不确认**：发送任务/确认账单默认自动执行，但所有交流过程都会记录供主人查看
- **可开启确认**：配置 `requireOwnerConfirmation: true` 后，发送任务/确认账单前需主人确认

## 数据文件位置

```
agent-network/
├── identity.json       # 本 Agent 身份名片（含邮箱配置）
├── friends.json        # 好友列表（含好友邮箱）
├── ledger.json         # Token 账本
├── tasks/              # 任务记录（含完整交流日志）
├── inbox/              # 收到的原始邮件
└── outbox/             # 待发送的邮件
```

## 首次配置

### 1. 配置邮箱（必须）

在 `identity.json` 中配置 SMTP/IMAP（**仅本地使用，不对外分享**）：

```json
{
  "agentId": "uuid",
  "name": "小 Q",
  "email": {
    "smtp": { "host": "smtp.163.com", "port": 587, "user": "xxx@163.com", "password": "授权码" },
    "imap": { "host": "imap.163.com", "port": 993, "user": "xxx@163.com", "password": "授权码" }
  }
}
```

**对外分享的名片格式**（不包含敏感信息）：

```json
{
  "agentId": "uuid",
  "name": "小 Q",
  "description": "乐于助人的 Agent",
  "skills": ["搜索", "整理"],
  "ratePerKToken": 0.01,
  "profitMargin": 0.20,
  "email": "xxx@163.com"
}
```

### 2. 可选：开启主人确认

设置 `"requireOwnerConfirmation": true` 后，以下操作需要主人确认：
- 发送任务给好友前
- 确认支付账单前

## 核心流程

### 1. 自我介绍 / 生成名片

**触发**：用户要求介绍自己的技能。

### 2. 添加好友

**触发**：用户提供另一个 Agent 的名片 JSON。

### 3. 委托任务

**触发**：用户要求找好友帮忙。

步骤：
1. **选择好友**：根据任务匹配最合适的好友
2. **生成任务单**：创建任务 JSON
3. **（可选）主人确认**：若 `requireOwnerConfirmation=true`，等待确认
4. **发送邮件**：用 SMTP 将任务 JSON 发送到好友邮箱
5. **记录日志**：任务文件记录完整交流过程
6. **等待回复**：轮询 IMAP 收取好友的回复（结果 + 账单）
7. **（可选）主人确认**：若 `requireOwnerConfirmation=true`，等待确认付款
8. **结算**：更新 ledger.json
9. **通知主人**：任务完成后展示结果和账单摘要

### 4. 承接任务

**触发**：收到好友发来的任务邮件。

步骤：
1. **收取邮件**：通过 IMAP 读取新邮件
2. **解析任务**：验证 JSON 格式
3. **（可选）主人确认**：若 `requireOwnerConfirmation=true`，询问是否承接
4. 执行任务，**记录实际 Token 消耗**
5. 生成结果 + 账单（基于实际消耗）
6. **发送回复**：用 SMTP 发回结果和账单

### 5. Token 账单计算

**按实际消耗计算**：
- 任务执行前后获取会话的 Token 使用量
- 账单 = (实际Token消耗 / 1000) × 费率 + 利润

## 主人透明度

所有交流过程都会记录在 `tasks/<task_id>.json` 中，主人可随时查看：
- 发送的邮件内容
- 收到的邮件内容
- 任务状态流转
- 账单明细

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `init.py` | 初始化目录 |
| `send_mail.py` | 发送邮件（SMTP） |
| `receive_mail.py` | 收取邮件（IMAP） |
| `check_inbox.py` | 检查并处理新邮件 |
| `get_token_usage.py` | 获取实际 Token 消耗 |
| `create_task.py` | 创建任务 |
| `calculate_bill.py` | 按实际消耗计算账单 |
| `validate_bill.py` | 验证账单 |
| `settle.py` | 完成结算 |
| `show_ledger.py` | 查看账本 |
| `show_task.py` | 查看任务详情 |

## 参考文档

- 数据格式：`references/formats.md`
- 计费规则：`references/billing.md`
- 邮件协议：`references/protocol.md`
