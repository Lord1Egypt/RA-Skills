---
name: design-framework-sender
description: 设计框架自动生成套件（主控路由）：监听群消息 @mention，根据状态路由到对应子 skill
disable-model-invocation: true
metadata:
  {"openclaw": {"always": true}}
---

# 设计框架套件 - 主控路由

本 skill 是「设计框架自动生成套件」的入口，负责监听 Telegram 群消息并根据当前任务状态路由到对应的子 skill。

## 套件组成

本套件共 4 个 skill，需全部安装后配合使用：

| Skill | 职责 |
|---|---|
| `design-framework-sender` | 主控路由（本 skill） |
| `design-framework-builder` | 生成设计框架 + 发群预览 |
| `design-framework-confirm` | 处理确认/取消/重新生成 |
| `design-framework-generate` | 生图 + 私发 + 完成通知 |

## 安装配置

### 1. 安装全部 4 个 skill

```bash
openclaw skills install design-framework-sender
openclaw skills install design-framework-builder
openclaw skills install design-framework-confirm
openclaw skills install design-framework-generate
```

### 2. 修改 config.py（唯一需要配置的文件）

编辑 `design-framework-sender/config.py`，填入自己的参数：

```python
"group_chat_id": design.get("group_chat_id", "你的Telegram群组ID"),
"bot_owner_id":  design.get("bot_owner_id",  "你的Telegram用户ID"),
```

### 3. 启用并重启

```json
{
  "skills": {
    "entries": {
      "design-framework-sender":  {"enabled": true},
      "design-framework-builder": {"enabled": true},
      "design-framework-confirm": {"enabled": true},
      "design-framework-generate": {"enabled": true}
    }
  }
}
```

```bash
openclaw gateway restart
```

## 工作流程

```
群消息含 @mention
      ↓
  [主控路由] ← 本 skill
  判断锁文件
      ↓
 ┌────┴────┐
不存在     存在
  ↓         ↓
builder   confirm
生成框架   处理回复
  ↓         ↓ 确认
发预览    generate
         生图交付
```

## 前置要求

- OpenClaw 已配置 Telegram Bot
- OpenRouter API Key 已配置
- Telegram Bot 已加入目标群组
