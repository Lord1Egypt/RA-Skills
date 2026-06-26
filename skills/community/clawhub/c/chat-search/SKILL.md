---
name: chat-search
description: use this when the user wants to search chat history, find conversations, or look up previous messages from feishu or telegram. triggers include: "搜索", "搜素", "查找", "找一下", "帮我搜", "查找聊天记录"
---

# Chat Search Skill

飞书/Telegram 聊天记录语义搜索

## 功能

- 语义搜索聊天记录
- 支持中文分词
- 显示相似度分数
- 区分消息来源（飞书/Telegram）
- 使用 Qdrant 向量数据库
- 使用 FastEmbed 生成中文向量

## 触发方式

当用户说以下内容时自动触发：
- "搜索XXX" / "搜素XXX" / "查找XXX"
- "帮我搜一下XXX"
- "找一下关于XXX的对话"

## 依赖

- Qdrant 向量数据库 (localhost:6333)
- Python FastEmbed (BGE 中文模型)
- Node.js

## 使用示例

```
用户：帮我搜索 Docker 相关的对话
小T：→ 执行搜索

🔍 搜索 "Docker" 的结果：

1. 🐦 [feishu] 小T (2026-03-20 09:17)
   Docker 安装成功了
   相似度: 58.2%
```

## 安装

需要先安装依赖：
```bash
# Qdrant
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant

# Python FastEmbed
pip install fastembed
```
