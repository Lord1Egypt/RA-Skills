# Context Manager Skill

长上下文管理器技能。为多个 AI Agent 提供智能的长期记忆管理，通过向量索引和时间轴双重命中判断，大幅减少 LLM 调用次数。

## 🎯 适用场景

当用户需要：
- 管理多个 Agent 的文件和上下文
- 在大型项目中快速检索相关信息
- 减少 LLM 调用以降低成本
- 建立长期记忆系统
- 在多个 Agent 之间共享上下文
- 基于语义相似度搜索文件
- 按时间维度过滤和检索内容

## 📋 功能清单

### Agent 管理
- 创建新的 Agent
- 查看 Agent 列表
- 获取 Agent 详情
- 删除 Agent

### 文件管理
- 为 Agent 创建文件
- 获取文件内容
- 列出 Agent 的所有文件
- 删除文件

### 智能检索
- 语义向量搜索
- 时间轴过滤
- 双重命中判断（向量+时间）
- 智能调取详情
- LLM 集成（可选）

## 🚀 使用方法

### 基本用法

#### 创建 Agent
```
为项目 "文档编写" 创建一个 Agent
```

#### 创建文件
```
将以下内容保存到 Agent "agent001" 的文件 "设计文档.md" 中：
[文件内容]
```

#### 查询
```
在 Agent "agent001" 中搜索 "深度学习算法"
```

#### 查询（带详情）
```
查找 "微服务架构设计" 相关内容，并获取详情
```

#### 列出文件
```
显示 Agent "agent001" 的所有文件
```

### 高级用法

#### 带标签的文件
```
创建一个关于 "机器学习" 的文件，标签为 "research, ai, ml"
```

#### 跨 Agent 搜索
```
在所有 Agent 中搜索 "Python 编程"
```

#### 强制 LLM 调用
```
用 LLM 分析 "如何优化数据库查询" 相关内容
```

## 🔧 配置

### 环境变量（可选）

```bash
# OpenAI API Key（用于 LLM 功能）
export OPENAI_API_KEY="your-api-key"

# Redis 配置（用于缓存）
export CONTEXT_MANAGER_REDIS_HOST="localhost"
export CONTEXT_MANAGER_REDIS_PORT=6379
```

### 配置参数（可选）

在 `config.py` 中可调整：

- `vector_threshold`: 向量相似度阈值（默认 0.7）
- `time_threshold`: 时间相关性阈值（默认 0.5）
- `combined_threshold`: 综合评分阈值（默认 0.6）
- `cache_ttl`: 缓存过期时间（默认 3600 秒）

## 📊 工作原理

### 文件索引流程
1. 接收文件内容
2. 生成向量嵌入
3. 存储到向量数据库
4. 提取时间轴信息
5. 更新索引

### 智能检索流程
1. 向量搜索找到相关文件
2. 时间轴过滤
3. 双重命中判断
4. 智能调取详情
5. LLM 集成（如需要）

## 💡 最佳实践

1. **文件命名**：使用有意义的文件名
2. **标签使用**：为文件添加相关主题标签
3. **时间标签**：使用时间标签帮助时间轴匹配
4. **批量操作**：批量创建文件以提高效率
5. **定期清理**：删除不再需要的文件

## ⚠️ 注意事项

- 文件内容会进行向量嵌入，需要网络连接（首次）
- LLM 功能需要配置 OpenAI API Key
- Redis 可选，未配置时使用内存缓存
- 向量数据库存储在本地 `vector_db` 目录

## 🔄 数据存储

所有数据存储在：
```
~/.openclaw-autoclaw/workspace/context-manager/
├── agents/           # Agent 数据
├── vector_db/        # 向量数据库
├── cache/            # 缓存数据
└── logs/             # 日志文件
```

## 📈 性能优化

预期效果：
- LLM 调用减少：60-80%
- 检索速度提升：10-50 倍
- 项目完成度显著提高

## 🔍 技术栈

- **向量数据库**: ChromaDB
- **嵌入模型**: Sentence Transformers
- **缓存**: Redis + 内存
- **API**: FastAPI
- **LLM**: OpenAI GPT（可选）

## 🛠️ 故障排除

### 问题：向量数据库初始化失败
解决：删除 `vector_db` 目录后重试

### 问题：Redis 连接失败
解决：系统会自动使用内存缓存

### 问题：LLM 调用超时
解决：检查网络连接和 API Key 配置

## 📚 示例对话

```
用户：为 "研究项目" 创建一个 Agent
AI：✓ 已创建 Agent "research-project"

用户：将以下内容保存到研究项目的文件 "文献综述.md"：
深度学习是机器学习的一个子集...
AI：✓ 文件 "文献综述.md" 已创建并索引（索引时间: 452ms）

用户：在研究项目中搜索 "神经网络"
AI：找到 3 个相关文件：
1. 文献综述.md（相似度: 0.89）
2. 算法总结.md（相似度: 0.76）
3. 项目计划.md（相似度: 0.65）

用户：获取 "神经网络" 相关内容的详情
AI：已获取 2 个文件的详情。LLM 回复：
[详细答案]
```

## 🎓 更多信息

查看完整文档：
`cat ~/.openclaw-autoclaw/workspace/context-manager/README.md`

运行示例：
`python ~/.openclaw-autoclaw/workspace/context-manager/example.py`

## 🔗 相关技能

- `memory` - 简单的内存管理
- `wecom-doc` - 企业微信文档管理
