---
name: byted-viking-developer
description: 指导开发者接入与使用Viking SDK, 覆盖 Viking 向量库、知识库、记忆库的安装、鉴权、接口调用与问题诊断, 当用户需要调用Viking SDK进行业务代码开发和Viking相关问题问答时使用.
---

## 使用场景
本skill需要配合Trae、OpenCode、Codex、Claude Code、Antigravity等工具使用，不支持OpenClaw场景。


## Viking 开发者助手

本 Skill 旨在帮助开发者快速接入和使用 Viking 平台的 SDK，涵盖向量数据库 (VikingDB)、知识库 (KnowledgeBase) 和记忆库 (Memory) 三大核心能力。

请根据您的具体需求，选择对应的 SDK 指引：

### 1. 向量库 SDK (VikingDB)
适用于需要高性能向量检索、标量检索、数据存储与管理的场景。支持 Python、Golang、Java 多语言接入。
- **核心功能**: Collection/Index 管理、数据 CRUD、向量/标量检索、多模态检索等。
- **多语言指引**:
  - [Python SDK 文档导引](resources/vikingdb-python-sdk.md)
  - [Go SDK 文档导引](resources/vikingdb-go-sdk.md)
  - [Java SDK 文档导引](resources/vikingdb-java-sdk.md)
- **辅助导引**:
  - [常见问题导引](resources/vikingdb-qa.md)
  - [性能优化导引](resources/vikingdb-performance-optim.md)
  - [最佳实践导引](resources/vikingdb-best-practice.md)
  - [其他文档导引](resources/vikingdb-other.md)

### 2. 知识库 SDK (KnowledgeBase)
适用于构建 RAG (检索增强生成)、文档管理、智能问答等场景。
- **核心功能**: 文档解析与管理、切片 (Point) 管理、全文/混合检索、RAG 生成、对话补全等。
- **多语言指引**:
  - [Python SDK 文档导引](resources/knowledge-python-sdk.md)
  - [Go SDK 文档导引](resources/knowledge-go-sdk.md)
- **辅助导引**:
  - [常见问题导引](resources/knowledge-qa.md)
  - [其他文档导引](resources/knowledge-other.md)
  - [SDK 升级与使用说明](resources/Viking%20%E7%9F%A5%E8%AF%86%E5%BA%93/SDK%E5%8F%82%E8%80%83/SDK%20%E5%8D%87%E7%BA%A7%E4%B8%8E%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.md)

### 3. 记忆库 SDK (Memory)
适用于构建具备长期记忆能力的 AI Agent，支持存储和检索用户画像及事件记忆。
- **核心功能**: Session 管理、事件记忆 (Event)、用户画像 (Profile)、记忆检索等。
- **多语言指引**:
  - [Python SDK 文档导引](resources/memory-python-sdk.md)
- **辅助导引**:
  - [最佳实践导引](resources/memory-best-practice.md)
  - [其他文档导引](resources/memory-other.md)
