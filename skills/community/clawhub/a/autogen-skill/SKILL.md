---
name: autogen
description: Microsoft AutoGen - 多智能体协同框架，用于构建复杂游戏设计工作流
homepage: https://github.com/microsoft/autogen
category: ai
tags: [multi-agent, gamedev, ai, microsoft, framework]
---

# AutoGen Skill

Microsoft AutoGen 多智能体框架的 OpenClaw 技能封装。

## 安装

已预装在 `/workspace/skills/gamedev-tools/autogen/`

## 使用

```python
import autogen

# 创建助手
assistant = autogen.AssistantAgent(
    name="game_designer",
    llm_config={"model": "gpt-4"}
)

# 创建用户代理
user_proxy = autogen.UserProxyAgent(
    name="user",
    human_input_mode="NEVER"
)

# 开始对话
user_proxy.initiate_chat(
    assistant,
    message="设计一个RPG游戏的第一章剧情"
)
```

## 路径

- 源码: `/workspace/skills/gamedev-tools/autogen/`
- Python包: 通过 `pip install pyautogen` 安装
