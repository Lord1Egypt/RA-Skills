---
name: feishu-message-group-whitelist
description: 飞书群聊白名单关键词过滤。当飞书机器人收到群消息时，根据白名单判断是否需要回复——只有消息中包含白名单关键词时才触发回复，实现精准触发而非广播所有消息。触发词示例：群里有人发消息时、提到特定关键词时、需要过滤无关消息时。
---

# Feishu Message Group Whitelist

## Overview

飞书群消息白名单过滤 Skill。机器人在群聊中收到消息时，读取白名单配置文件，**仅当消息正文包含白名单中的关键词时才触发正常回复流程**，否则静默跳过。

白名单配置为独立文件，方便随时增删关键词，无需修改 Skill 逻辑。

## Core Logic

收到飞书群消息时：

```
1. 读取 config/whitelist.txt（每行一个关键词，去除空格和空行）
2. 若白名单为空 → 跳过过滤，正常回复（兼容未配置场景）
3. 遍历白名单关键词，若消息正文包含某关键词 → 触发正常回复
4. 若所有关键词均不匹配 → 静默返回 HEARTBEAT_OK，不消耗 token
```

## Whitelist Config

白名单文件路径：`config/whitelist.txt`

格式：每行一个关键词，支持任意字符，支持中英文混合。

示例：
```
高斯
CAO
报告
分析
```

## Message Flow

```
飞书群消息到达
  → 检查 whitelist.txt 是否有匹配
     → 有匹配：进入正常 Agent 响应流程
     → 无匹配：返回 NO_REPLY，静默跳过
```

## Config Location

- 白名单文件：`config/whitelist.txt`（相对于 skill 根目录）
- Skill 根目录由 OpenClaw 加载时确定，通常为 `~/.openclaw/skills/feishu-message-group-whitelist/` 或 workspace 下的对应目录

首次使用时请在白名单中添加需要的触发关键词。
