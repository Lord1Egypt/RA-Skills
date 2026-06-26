# Dify 知识库配置

## 创建知识库

### 索引模式

| 模式 | 说明 | 适用场景 |
|-----|------|---------|
| High Quality | 高质量索引，使用Embedding模型 | 需要语义检索 |
| Economy | 经济模式，关键词索引 | 简单检索，无Embedding成本 |

### 文档处理

**分段设置:**
- Automatic - 自动分段
- Custom - 自定义规则

**分段参数:**
- 分段标识符: `\n\n`, `\n`, 句号等
- 最大分段长度: 默认1000 tokens
- 重叠长度: 默认50 tokens

**预处理:**
- 清理无用字符
- 替换连续空格和换行

---

## 检索模式

### Vector Search (向量检索)

使用Embedding向量计算语义相似度:

**参数:**
- Top K: 返回结果数量 (1-10)
- Score Threshold: 相似度阈值 (0-1)
- Embedding Model: 向量化模型

### Full Text Search (全文检索)

关键词匹配检索:

**参数:**
- Top K
- Score Threshold

### Hybrid Search (混合检索)

结合向量和全文检索:

**参数:**
- Top K
- Score Threshold
- 权重配置

---

## 文档管理

### 支持格式

| 类型 | 格式 |
|-----|------|
| 文本 | txt, markdown, md, pdf, docx, html, xlsx, xls |
| 图片 | jpg, jpeg, png, gif, webp (需Vision模型) |
| 音频 | mp3, wav, m4a (需Whisper) |

### 文档状态

- **Waiting** - 等待处理
- **Indexing** - 正在索引
- **Completed** - 完成
- **Error** - 错误
- **Paused** - 暂停

### 批量操作

- 批量上传
- 批量删除
- 重新索引

---

## 高级配置

### Embedding模型

支持多种Embedding模型:
- OpenAI text-embedding-3-small/large
- Cohere embed-multilingual
- 本地模型 (需自托管)

### Rerank模型

可选的重排序模型，提高检索精度:
- Cohere rerank-multilingual
- Jina rerank

### 召回测试

在知识库页面测试检索效果:
1. 输入查询
2. 查看召回的分段
3. 调整参数优化

---

## 最佳实践

### 文档准备
1. 结构化文档标题和段落
2. 避免过长的单个段落
3. 保持内容的语义完整性

### 分段策略
1. 按段落或章节分段
2. 保持上下文连贯
3. 适当设置重叠长度

### 检索优化
1. 使用混合检索提高召回
2. 根据场景调整Top K
3. 测试不同阈值
