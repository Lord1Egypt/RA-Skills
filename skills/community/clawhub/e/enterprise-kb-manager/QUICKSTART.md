# 企业知识库快速开始指南

## 📋 系统要求

- Python 3.8+
- 8GB+ 内存 (推荐)
- 1GB+ 磁盘空间

## 🚀 安装步骤

### 1. 安装依赖

```bash
cd skills/kb-manager
pip install -r requirements.txt
```

如果遇到安装问题：
```bash
# 升级pip
python -m pip install --upgrade pip

# 强制重新安装
pip install -r requirements.txt --force-reinstall
```

### 2. 配置API密钥

**推荐：DashScope (阿里云千问)**
```powershell
$env:DASHSCOPE_API_KEY='sk-your-dashscope-key-here'
```

**或者：OpenAI**
```powershell
$env:OPENAI_API_KEY='sk-your-openai-key-here'
```

**持久化配置 (可选)**
编辑 `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "kb-manager": {
        "enabled": true,
        "env": {
          "DASHSCOPE_API_KEY": "your-key-here"
        },
        "config": {
          "embeddingProvider": "dashscope",
          "embeddingModel": "text-embedding-v3",
          "chunkSize": 500,
          "retrievalTopK": 5
        }
      }
    }
  }
}
```

### 3. 验证安装

**测试API连接**
```bash
python test_dashscope.py
```
预期输出：
```
Testing DashScope API integration...
✓ API key found: sk-2450c10...
✓ Config loaded - Provider: dashscope
Testing embedding for: '这是一个测试文档'
✅ Success! Generated 1536 dimensional vector
First 5 values: [0.123, -0.456, 0.789, ...]
```

**完整系统测试**
```bash
python test_system.py
```
预期输出：
```
============================================================
Enterprise Knowledge Base - System Test
============================================================

1️⃣  Loading configuration...
   ✓ Chunk size: 500
   ✓ Embedding model: text-embedding-v3
   ✓ Milvus URI: ./data/chroma_db

2️⃣  Initializing components...
   ✓ Document processor ready
   ✓ Retriever ready
   ✓ Manager ready

3️⃣  Creating test document...
   ✓ Created test_company_policy.txt

4️⃣  Processing document...
📄 Parsing test_company_policy.txt...
✂️  Chunking document...
   Created 3 chunks
🔢 Generating embeddings...
💾 Storing in vector database...
   ✓ Successfully processed test_company_policy.txt: 3 chunks created

5️⃣  Knowledge base statistics...
   ✓ Total documents: 1
   ✓ Total chunks: 3
   ✓ Storage size: 0.01 MB

6️⃣  Testing retrieval...
   Query: 公司的年假政策是什么？
   ✓ Found 2 relevant chunks:
     [1] Score: 0.856 | 员工每年享有15天带薪年假。年假需要提前一周申请，并获得主管批准。...
     [2] Score: 0.743 | 公司休假政策...

============================================================
✅ All tests passed!
============================================================
```

## 📖 使用示例

### 在OpenClaw中使用

**1. 上传文档**
```
用户: [附件: 公司手册.pdf] 上传到知识库
AI: ✅ 文档上传成功！已处理 公司手册.pdf，创建了 45 个文档块。
```

**2. 智能问答**
```
用户: 公司的休假政策是什么？
AI: 根据公司手册，休假政策如下：

📋 年假政策：
- 员工每年享有15天带薪年假
- 需要提前一周申请并获得主管批准
- 年假不可跨年累积

🏥 病假政策：
- 每年有10天带薪病假
- 超过3天需要提供医生证明

🏠 远程办公：
- 每周可远程办公2天
- 需要提前向主管报备

来源：公司手册.pdf
```

**3. 文档管理**
```
用户: list kb documents
AI: 📚 知识库文档列表：

1. 公司手册.pdf (45 chunks)
2. 员工守则.docx (23 chunks)  
3. 技术规范.md (67 chunks)

总计：3个文档，135个文档块
```

### Python API使用

```python
from src import load_config, DocumentProcessor, Retriever, ChromaVectorDB, Embedder

# 1. 加载配置
config = load_config()
print(f"使用嵌入模型: {config.embedding_model}")

# 2. 初始化组件
processor = DocumentProcessor(config)
db = ChromaVectorDB(
    db_path=config.milvus_uri,
    collection_name=config.collection_name
)
embedder = Embedder(
    model=config.embedding_model,
    api_key=config.embedding_api_key,
    provider=config.embedding_provider,
    base_url=config.embedding_base_url
)
retriever = Retriever(db, embedder, top_k=config.retrieval_top_k)

# 3. 上传文档
result = processor.process_document("company_policy.pdf", "公司政策")
if result.success:
    print(f"✅ {result.message}")
    print(f"文档ID: {result.document_id}")
    print(f"创建块数: {result.chunk_count}")
else:
    print(f"❌ 上传失败: {result.error}")

# 4. 搜索查询
query = "休假政策"
results = retriever.retrieve(query, top_k=3)

print(f"\n🔍 搜索 '{query}' 的结果:")
for i, r in enumerate(results):
    print(f"[{i+1}] 相似度: {r.score:.3f}")
    print(f"    文档: {r.document_name}")
    print(f"    内容: {r.text[:100]}...")
    print()

# 5. 格式化上下文 (用于LLM)
context = retriever.format_context(results)
print("📝 格式化的上下文:")
print(context)
```

## 🔧 故障排除

### 常见问题

**1. API密钥错误**
```bash
❌ Error: Invalid API key
```
解决方案：
```bash
# 检查环境变量
echo $env:DASHSCOPE_API_KEY

# 重新设置
$env:DASHSCOPE_API_KEY='your-correct-key'

# 测试连接
python test_dashscope.py
```

**2. 依赖安装失败**
```bash
❌ Error: Failed to build grpcio
```
解决方案：
```bash
# 使用ChromaDB (无需grpcio)
pip uninstall pymilvus
pip install chromadb>=0.4.0

# 或者使用预编译版本
pip install --only-binary=grpcio grpcio
```

**3. 文档解析失败**
```bash
❌ Error: Unsupported file format
```
解决方案：
```bash
# 检查支持的格式
python -c "from src.parser import DocumentParser; print(DocumentParser.SUPPORTED_FORMATS)"

# 转换文档格式
# PDF → TXT: 使用在线转换工具
# DOCX → TXT: 另存为文本文件
```

**4. 数据库连接问题**
```bash
❌ Error: Database connection failed
```
解决方案：
```bash
# 重置数据库
Remove-Item -Recurse -Force ./data/chroma_db

# 重新初始化
python test_system.py
```

**5. 内存不足**
```bash
❌ Error: Out of memory
```
解决方案：
```bash
# 减小分块大小
# 在config.json中设置:
{
  "chunkSize": 300,
  "chunkOverlap": 30
}

# 或者分批处理大文档
```

### 性能优化

**1. 提高处理速度**
```json
{
  "chunkSize": 800,        // 增大分块 (减少块数)
  "chunkOverlap": 80,      // 保持10%重叠
  "retrievalTopK": 3       // 减少检索结果数
}
```

**2. 提高搜索精度**
```json
{
  "chunkSize": 300,        // 减小分块 (更精确)
  "chunkOverlap": 50,      // 增加重叠 (更完整)
  "retrievalTopK": 8       // 增加检索结果数
}
```

**3. 节省存储空间**
```json
{
  "vectorDimension": 768,  // 使用较小的嵌入模型
  "embeddingModel": "text-embedding-ada-002"
}
```

## 📊 监控与维护

### 查看系统状态
```bash
# 获取统计信息
python -c "
from src import load_config, KnowledgeBaseManager, ChromaVectorDB
config = load_config()
db = ChromaVectorDB(config.milvus_uri, config.collection_name)
manager = KnowledgeBaseManager(db, config.documents_dir)
stats = manager.get_statistics()
for k, v in stats.items():
    print(f'{k}: {v}')
"
```

### 数据备份
```bash
# 备份向量数据库
Copy-Item -Recurse ./data/chroma_db ./backup/chroma_db_$(Get-Date -Format 'yyyyMMdd')

# 备份文档
Copy-Item -Recurse ./documents ./backup/documents_$(Get-Date -Format 'yyyyMMdd')
```

### 清理数据
```bash
# 清理所有数据
Remove-Item -Recurse -Force ./data/chroma_db
Remove-Item -Recurse -Force ./documents/kb-manager

# 重新初始化
python test_system.py
```

## 🎯 下一步

1. **查看完整文档**: 阅读 `README.md` 了解系统架构
2. **配置优化**: 根据使用场景调整 `config.json` 参数  
3. **集成OpenClaw**: 将技能添加到OpenClaw配置中
4. **批量上传**: 准备企业文档并批量上传到知识库
5. **用户培训**: 培训团队成员使用知识库问答功能

## 📞 获取帮助

- 🐛 **问题诊断**: 运行 `python test_system.py`
- 📖 **详细文档**: 查看 `SKILL.md` 和 `README.md`
- 💡 **功能建议**: 提交GitHub Issue
- 🔧 **技术支持**: 查看源码注释和文档字符串
