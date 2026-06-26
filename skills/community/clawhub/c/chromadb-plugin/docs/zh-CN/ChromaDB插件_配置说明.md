# ChromaDB官方插件 - 配置说明
## 🔧 完整配置项说明
所有配置均在`config.yaml`的`vector_store`节点下配置，修改后重启服务自动生效。

### 基础配置
```yaml
vector_store:
  # 向量库类型，可选值：lancedb / chromadb
  type: chromadb
  # 本地存储路径（本地模式使用）
  path: "I:/OpenClaw/知识库/chromadb"
  # 向量模型名称，保持和现有BGE-M3一致即可
  model: "BAAI/bge-m3"
  # 向量维度，BGE-M3固定为1024，无需修改
  dimension: 1024
```

### 云端ChromaDB配置（可选）
如果使用云端部署的ChromaDB服务，替换配置即可：
```yaml
vector_store:
  type: chromadb
  # 云端服务地址
  host: "https://your-chromadb-service.com"
  # 端口（默认8000）
  port: 8000
  # API密钥（如果开启认证）
  api_key: "your-api-key"
  # 租户名称（多租户部署使用）
  tenant: "default_tenant"
  # 数据库名称
  database: "default_database"
```

### 性能优化配置
```yaml
vector_store:
  # 是否开启GPU加速（默认开启，有CUDA环境自动启用）
  gpu_accelerate: true
  # 批量写入最大批次大小
  batch_size: 1000
  # 检索返回最大结果数
  top_k: 10
  # 相似度阈值（低于该分数的结果自动过滤）
  similarity_threshold: 0.5
  # 向量索引类型，可选：HNSW / IVF_FLAT / IVF_PQ（默认HNSW，平衡速度和准确率）
  index_type: HNSW
  # HNSW索引参数，根据数据量调整
  hnsw_config:
    M: 16
    ef_construction: 200
    ef_search: 50
```

### 高级功能配置
```yaml
vector_store:
  # 是否开启自动持久化（默认开启，每次写入自动落盘）
  auto_persist: true
  # 自动持久化间隔（毫秒）
  persist_interval: 1000
  # 是否开启向量压缩（默认开启，节省存储空间）
  vector_compression: true
  # 压缩等级，0-9，越高压缩比越高，速度越慢
  compression_level: 3
  # 日志级别，可选：DEBUG / INFO / WARN / ERROR
  log_level: INFO
```

## 📝 配置示例
### 本地开发环境配置（推荐）
```yaml
vector_store:
  type: chromadb
  path: "I:/OpenClaw/知识库/chromadb"
  model: "BAAI/bge-m3"
  gpu_accelerate: true
  top_k: 10
  similarity_threshold: 0.5
```

### 生产环境高可用配置
```yaml
vector_store:
  type: chromadb
  host: "http://192.168.1.100"
  port: 8000
  api_key: "your-production-api-key"
  gpu_accelerate: true
  batch_size: 2000
  hnsw_config:
    M: 32
    ef_construction: 300
    ef_search: 100
  auto_persist: true
  persist_interval: 5000
```

## ⚙️ 环境变量配置（适合容器部署）
也可以通过环境变量配置，优先级高于配置文件：
| 环境变量 | 说明 |
|----------|------|
| CHROMADB_HOST | 云端服务地址 |
| CHROMADB_PORT | 服务端口 |
| CHROMADB_API_KEY | API密钥 |
| CHROMADB_TENANT | 租户名称 |
| CHROMADB_DATABASE | 数据库名称 |
| CHROMADB_GPU_ACCELERATE | 是否开启GPU加速（true/false） |

---
**文档版本**: v1.0.0
**更新时间**: 2026-03-29 13:25
**作者**: 岚岚
