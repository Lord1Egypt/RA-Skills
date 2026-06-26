---
name: feishu-repair
description: 自动修复飞书-自动修复飞书群聊+自动修复会话 - 诊断 Gateway 连接、权限配置、消息投递问题
version: 2.0.0
author: c32
category: monitoring
tags:
  - feishu
  - repair
  - group-chat
  - session
requirements:
  node: ">=18.0.0"
  systemd: true
---

# Feishu Repair — 飞书群聊+会话修复技能

**版本**: 1.9.0
**创建日期**: 2026-04-14
**触发关键词**: `修复飞书`

---

## 📋 功能

自动诊断和修复 OpenClaw 飞书渠道的常见问题：

| 问题类型 | 诊断方式 | 修复方式 |
|---------|---------|---------|
| Gateway 未运行 | systemctl 检查 | 自动重启 Gateway |
| 飞书 WebSocket 断开 | journalctl 日志 | 自动重启 Gateway |
| 群聊权限丢失 | 检查 groupAllowFrom | 自动恢复配置 + 强制重启 + 验证 + 发送消息到所有群聊和用户 |
| 用户权限丢失 | 检查 allowFrom | 自动恢复配置 + 强制重启 + 验证 + 发送消息到所有群聊和用户 |
| 配置未生效 | 检查 config | 强制重启 Gateway + 验证 |
| 消息不回复 | 综合诊断 | 输出修复报告 + 发送验证消息 |

---

## 📂 文件结构

```
skills/feishu-repair/
├── SKILL.md
├── skill.json
├── _meta.json
└── scripts/
    └── diagnose.js     # 诊断脚本
```

---

## 🔧 修复流程

```
诊断 → 修复 → 强制重启 Gateway → 验证 → 发消息确认
```

| 步骤 | 功能 | 说明 |
|------|------|------|
| 1️⃣ 诊断 | 检查 Gateway、飞书配置、日志错误 | 始终执行 |
| 2️⃣ 修复 | 从配置恢复丢失的权限 | 检测到问题 |
| 3️⃣ **强制重启** | 重启 Gateway 使配置生效 | **有修复操作时强制重启** |
| 4️⃣ 验证 | 配置 + 日志双重检查 | 重启后自动执行 |
| 5️⃣ 消息确认 | 遍历所有群聊和会话发送当前时间 | 验证通过后自动发送 |

### 修复策略

| 策略 | 触发条件 | 动作 |
|------|---------|------|
| 配置恢复 | 权限丢失/配置异常 | 从 `openclaw.json` 或 `openclaw.json.bak*` 读取完整配置自动恢复 |
| Gateway 状态检查 | Gateway 未运行 | 自动重启 Gateway |
| WebSocket 重连 | WS 断开日志 | 自动重启 Gateway |
| 配置生效检查 | 配置变更未生效 | 自动重启 Gateway + 验证 |

### 配置读取优先级

1. **`~/.openclaw/openclaw.json`**（当前配置）
2. **`~/.openclaw/openclaw.json.bak`**（最新备份）
3. **`~/.openclaw/openclaw.json.bak.1`**（更早备份）

按顺序读取，找到第一个有飞书配置的文件即停止。从中提取 `allowFrom`、`groupAllowFrom`、`appId` 等完整列表。

---

## 📊 配置来源

技能内**不硬编码**任何用户 ID、群聊 ID、App ID。

全部从用户的 `openclaw.json` 及其备份文件中动态读取。

---

## ⚠️ 注意事项

- 检测到配置问题并修复后，**强制重启 Gateway**（不是提示手动）
- 重启完成后，自动验证修复结果（配置 + 日志双重检查）
- 验证通过后，自动在飞书所有群聊（groupAllowFrom）和会话（allowFrom）发送当前时间，确认消息功能已恢复
- 配置读取优先级：`openclaw.json` > `openclaw.json.bak` > `openclaw.json.bak.1`
- 诊断结果输出详细报告
