---
name: email-auto-reply
version: 1.0.0
description: 邮件自动回复工具。根据关键词匹配自动回复，支持常见问题模板。适合客服和忙碌人士。
author: 你的名字
triggers:
  - "自动回复"
  - "邮件回复"
  - "邮件模板"
  - "自动回复邮件"
---

# Email Auto Reply 📧

邮件自动回复工具，根据关键词匹配自动回复。

## 功能

- 📝 关键词自动回复
- 📋 模板管理
- 🔄 多账号支持
- ✅ 自动抄送

## 使用方法

### 添加回复规则

```bash
python3 scripts/auto_reply.py add "关键词" "回复内容"
```

### 列出规则

```bash
python3 scripts/auto_reply.py list
```

### 删除规则

```bash
python3 scripts/auto_reply.py delete 1
```

### 测试回复

```bash
python3 scripts/auto_reply.py test "你好，我想咨询"
```

## 示例

```bash
# 添加自动回复
python3 scripts/auto_reply.py add "价格" "感谢咨询，我们的价格请访问官网..."

python3 scripts/auto_reply.py add "退款" "您的退款申请已收到，我们将在3个工作日内处理..."

# 测试
python3 scripts/auto_reply.py test "我想问价格"
```
