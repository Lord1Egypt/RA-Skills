# 知识库只读查询器 (KB Reader)

专门用于查询和读取企业知识库内容的轻量级系统，不支持文档上传和管理功能。

## 特性

- ✅ **只读访问**: 仅支持查询和读取，确保知识库安全
- ✅ **智能搜索**: 基于向量相似度和关键词匹配的混合搜索
- ✅ **轻量级**: 最小化依赖，专注查询功能
- ✅ **兼容性**: 可以读取kb-manager创建的知识库
- ✅ **多种查询模式**: 支持对话式查询和命令行查询

## 安装

1. 安装依赖：
```bash
cd skills/kb-reader
pip install -r requirements.txt
```

2. 配置API密钥：
```bash
export DASHSCOPE_API_KEY="your-api-key"
```

3. 配置知识库路径（编辑 config.json）：
```json
{
  "milvusUri": "系统自动配置",
  "documentsDir": "系统自动配置"
}
```

## 使用方法

### 对话模式
```bash
python main.py chat
```

### 直接查询
```bash
python main.py query "公司的休假政策是什么？"
```

### 详细搜索
```bash
python main.py search "蓝源军规"
```

### 查看文档列表
```bash
python main.py list
```

### 查看统计信息
```bash
python main.py stats
```

## 配置说明

主要配置项：

- `milvusUri`: 知识库向量数据库路径
- `documentsDir`: 文档存储目录
- `embeddingProvider`: 嵌入模型提供商 (dashscope/openai)
- `retrievalTopK`: 检索返回的结果数量
- `enableRerank`: 是否启用重排序

## 注意事项

1. 此工具仅支持只读操作，无法上传、删除或修改文档
2. 需要先使用 kb-manager 创建知识库
3. 确保配置的知识库路径正确
4. API密钥需要有效才能进行向量搜索

## AI Agent 集成

### OpenClaw 平台

在 OpenClaw 中使用：
```
@kb-reader query 公司政策
@kb-reader list
@kb-reader stats
```

### 其他平台

支持 Agent Skills 标准的平台：
- Kiro IDE
- Claude Code  
- 自定义 Agent 系统