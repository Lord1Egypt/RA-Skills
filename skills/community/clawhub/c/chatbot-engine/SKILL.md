---
name: chatbot-engine
description: 智能对话引擎 - 多轮对话与意图识别 | Chatbot Engine - Multi-turn dialogue and intent recognition
homepage: https://github.com/openclaw/chatbot-engine
category: nlp
tags: ["chatbot", "nlp", "dialogue", "intent-recognition", "conversation", "ai"]
---

# Chatbot Engine - 智能对话引擎

企业级对话系统解决方案，支持多轮对话、意图识别、上下文管理和知识库检索。

## 核心功能

| 功能模块 | 说明 |
|---------|------|
| **意图识别** | 基于规则/机器学习的意图分类 |
| **实体抽取** | 命名实体识别（人名、地点、时间等）|
| **多轮对话** | 上下文感知的多轮交互 |
| **知识库检索** | 基于向量检索的知识问答 |
| **对话管理** | 对话状态跟踪和流程控制 |

## 快速开始

```python
from scripts.dialogue_manager import DialogueManager

# 创建对话管理器
bot = DialogueManager()

# 处理用户输入
response = bot.process("我想预订明天北京的酒店")
print(response)
```

## 安装

```bash
pip install -r requirements.txt
```

## 项目结构

```
chatbot-engine/
├── SKILL.md                 # Skill说明文档
├── README.md                # 完整文档
├── requirements.txt         # 依赖列表
├── scripts/                 # 核心模块
│   ├── dialogue_manager.py  # 对话管理器
│   ├── intent_classifier.py # 意图分类器
│   ├── entity_extractor.py  # 实体抽取器
│   └── knowledge_base.py    # 知识库
├── examples/                # 使用示例
│   └── basic_usage.py
└── tests/                   # 单元测试
    └── test_chatbot.py
```
