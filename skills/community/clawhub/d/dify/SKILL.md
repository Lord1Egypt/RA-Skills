---
name: dify
description: Dify AI应用开发平台指南。用于构建LLM应用、工作流、Agent和知识库。当用户需要(1)使用Dify创建AI应用 (2)设计LLM工作流 (3)配置知识库RAG (4)开发AI Agent (5)调用Dify API (6)自托管部署Dify时激活此技能。
---

# Dify AI应用开发平台

Dify是开源的LLM应用开发平台，支持快速构建AI应用、工作流和Agent。

## 核心概念

### 应用类型
- **Chat App** - 对话型应用，支持会话持久化，适合聊天机器人、客服AI
- **Workflow App** - 工作流应用，无状态执行，适合翻译、写作、摘要
- **Agent** - 智能体应用，支持工具调用和自主规划
- **Completion App** - 文本补全应用，单次请求响应

### 核心组件
- **Studio** - 应用构建工作台
- **Knowledge Base** - 知识库，支持RAG检索增强
- **Model Providers** - 模型提供商配置
- **Tools** - 工具集成

## 工作流节点

### 输入输出
- **User Input** - 用户输入，定义输入变量
- **Output** - 输出结果

### 逻辑控制
- **IF/ELSE** - 条件分支
- **Iteration** - 迭代循环
- **Parallel** - 并行执行

### 数据处理
- **Parameter Extractor** - 参数提取，用LLM从自然语言提取结构化数据
- **List Operator** - 列表操作，过滤和转换数组
- **Variable Aggregator** - 变量聚合
- **Template** - 模板渲染

### LLM节点
- **LLM** - 大语言模型调用
- **Question Classifier** - 问题分类
- **Knowledge Retrieval** - 知识检索

### 工具节点
- **HTTP Request** - HTTP请求
- **Code** - 代码执行(Python/JavaScript)
- **Tool** - 工具调用

## 快速开始

### 部署Dify (Docker)

```bash
# 克隆最新版本
git clone --branch "$(curl -s https://api.github.com/repos/langgenius/dify/releases/latest | jq -r .tag_name)" https://github.com/langgenius/dify.git

# 启动
cd dify/docker
cp .env.example .env
docker compose up -d
```

访问 `http://localhost/install` 初始化管理员账户。

### 系统要求
- CPU >= 2 Core
- RAM >= 4 GiB
- Docker 19.03+
- Docker Compose 1.28+

## API调用

### 认证
所有API请求需要在Header中携带API Key:
```
Authorization: Bearer {api_key}
```

### 执行工作流
```bash
POST /v1/workflows/run
Content-Type: application/json

{
  "inputs": {
    "query": "翻译这段文字..."
  },
  "response_mode": "blocking",  # 或 "streaming"
  "user": "user-123"
}
```

### 发送聊天消息
```bash
POST /v1/chat-messages
Content-Type: application/json

{
  "query": "你好",
  "response_mode": "streaming",
  "user": "user-123",
  "conversation_id": ""  # 首次为空，后续传入返回的conversation_id
}
```

### 响应模式
- **blocking** - 同步等待完整响应
- **streaming** - SSE流式响应

## 知识库

### 创建知识库
1. Studio → Knowledge → Create Knowledge
2. 上传文档 (支持txt, markdown, pdf, docx, html等)
3. 选择索引模式:
   - **High Quality** - 高质量索引，需要Embedding模型
   - **Economy** - 经济模式，关键词检索

### 检索设置
- **Vector Search** - 向量检索
- **Full Text Search** - 全文检索
- **Hybrid Search** - 混合检索

### 在应用中使用
工作流中添加 Knowledge Retrieval 节点，选择知识库。

## 详细参考

- [API文档](references/api.md) - 完整API接口说明
- [工作流节点](references/workflow-nodes.md) - 所有节点详细配置
- [知识库配置](references/knowledge-base.md) - 知识库高级设置
- [模型配置](references/model-providers.md) - 支持的模型提供商

## 资源链接

- 官方文档: https://docs.dify.ai
- GitHub: https://github.com/langgenius/dify
- 社区: https://github.com/langgenius/dify/discussions
