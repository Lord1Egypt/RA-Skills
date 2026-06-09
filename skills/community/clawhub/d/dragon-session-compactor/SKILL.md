---
name: "Dragon Session Compactor"
description: "上下文压缩技能。当对话越来越长、token快爆的时候，自动压缩旧消息为摘要，保留最近上下文。 触发条件： - "压缩会话"、"compact"、"上下文满了" - 检测到消息超过阈值（默认100条或token估计超过80000） - 手动调用 $compact 无外部依赖，纯Node.js实现。"
category: "other"
source: "ClawHub"
tags: [compact, context, dragon, session, summary]
platforms: []
author: ""
version: ""
license: ""
installCmd: "hermes skills install clawhub/dragon-session-compactor"
sourceUrl: "https://clawhub.ai/skills/dragon-session-compactor"
---

# Dragon Session Compactor

> 上下文压缩技能。当对话越来越长、token快爆的时候，自动压缩旧消息为摘要，保留最近上下文。 触发条件： - "压缩会话"、"compact"、"上下文满了" - 检测到消息超过阈值（默认100条或token估计超过80000） - 手动调用 $compact 无外部依赖，纯Node.js实现。

- **Category:** Other
- **Source:** ClawHub
- **Author:** 
- **Version:** 
- **License:** 
- **Platforms:** All
- **Install Command:** `hermes skills install clawhub/dragon-session-compactor`
- **Source URL:** [https://clawhub.ai/skills/dragon-session-compactor](https://clawhub.ai/skills/dragon-session-compactor)

## Overview


## Installation
To install this skill, run the following command in your terminal:
```bash
hermes skills install clawhub/dragon-session-compactor
```
