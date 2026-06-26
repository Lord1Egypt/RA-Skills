# COS 向量桶全功能管理 Skill

> 腾讯云 COS 向量桶的 CodeBuddy AI Skill，覆盖向量桶、索引、向量数据的全生命周期管理，共 **16 个核心能力**。

## ✨ 功能概览

| 类别 | 能力 | 脚本 |
|------|------|------|
| **向量桶管理** | 创建向量桶 | `create_vector_bucket.py` |
| | 删除向量桶 | `delete_vector_bucket.py` |
| | 查询向量桶信息 | `get_vector_bucket.py` |
| | 列出所有向量桶 | `list_vector_buckets.py` |
| **桶策略管理** | 设置桶策略 | `put_vector_bucket_policy.py` |
| | 获取桶策略 | `get_vector_bucket_policy.py` |
| | 删除桶策略 | `delete_vector_bucket_policy.py` |
| **索引管理** | 创建索引 | `create_index.py` |
| | 查询索引信息 | `get_index.py` |
| | 列出所有索引 | `list_indexes.py` |
| | 删除索引 | `delete_index.py` |
| **向量数据操作** | 插入/更新向量 | `put_vectors.py` |
| | 获取指定向量 | `get_vectors.py` |
| | 列出向量列表 | `list_vectors.py` |
| | 删除向量 | `delete_vectors.py` |
| | 相似度搜索 | `query_vectors.py` |

---

## 🚀 快速开始

### 前置条件

- Python 3.6+
- 腾讯云 COS Python SDK

```bash
pip3 install cos-python-sdk-v5 --upgrade
```

### 验证安装

```bash
python3 -c "from qcloud_cos import CosConfig, CosVectorsClient; print('SDK 安装成功')"
```

### 准备凭证

你需要准备以下腾讯云凭证信息：

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| **SecretId** | API 密钥 ID | [腾讯云控制台 > API密钥管理](https://console.cloud.tencent.com/cam/capi) |
| **SecretKey** | API 密钥 Key | 同上 |
| **Region** | 存储桶区域 | 如 `ap-guangzhou`、`ap-shanghai`、`ap-beijing` |
| **Bucket** | 向量桶名称 | 格式 `BucketName-APPID`，如 `my-vectors-1250000000` |

凭证可通过两种方式提供：

**方式 1：命令行参数**
```bash
python3 scripts/list_vector_buckets.py \
  --secret-id "AKIDxxxxxxxxxxxx" \
  --secret-key "xxxxxxxxxxxxxxxx" \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000"
```

**方式 2：环境变量（推荐）**
```bash
export COS_VECTORS_SECRET_ID="AKIDxxxxxxxxxxxx"
export COS_VECTORS_SECRET_KEY="xxxxxxxxxxxxxxxx"

python3 scripts/list_vector_buckets.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000"
```

---

## 📖 使用指南

### 一、向量桶管理

#### 1. 创建向量桶

```bash
python3 scripts/create_vector_bucket.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --sse-type AES256    # 可选，启用 AES256 加密
```

#### 2. 查询向量桶信息

```bash
python3 scripts/get_vector_bucket.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000"
```

#### 3. 列出所有向量桶

```bash
python3 scripts/list_vector_buckets.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --max-results 20     # 可选，限制返回数量
  --prefix "my-"       # 可选，前缀过滤
```

#### 4. 删除向量桶

```bash
python3 scripts/delete_vector_bucket.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000"
```

### 二、桶策略管理

#### 5. 设置桶策略

```bash
python3 scripts/put_vector_bucket_policy.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --policy '{"Statement": [{"Effect": "Allow", "Principal": {"qcs": ["qcs::cam::uin/100000000001:uin/100000000001"]}, "Action": ["name/cos:*"], "Resource": ["qcs::cos:ap-guangzhou:uid/1250000000:my-vectors-1250000000/*"]}]}'
```

#### 6. 获取桶策略

```bash
python3 scripts/get_vector_bucket_policy.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000"
```

#### 7. 删除桶策略

```bash
python3 scripts/delete_vector_bucket_policy.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000"
```

### 三、索引管理

#### 8. 创建索引

```bash
python3 scripts/create_index.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --dimension 128 \
  --data-type float32 \
  --distance-metric cosine
```

| 参数 | 必需 | 说明 |
|------|:---:|------|
| `--index` | ✅ | 索引名称 |
| `--dimension` | ✅ | 向量维度（1-4096） |
| `--data-type` | ❌ | 数据类型，默认 `float32` |
| `--distance-metric` | ❌ | 距离度量：`cosine`（默认）或 `euclidean` |
| `--non-filterable-keys` | ❌ | 非过滤元数据键，逗号分隔 |

#### 9. 查询索引信息

```bash
python3 scripts/get_index.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index"
```

#### 10. 列出所有索引

```bash
python3 scripts/list_indexes.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --max-results 10
```

#### 11. 删除索引

```bash
python3 scripts/delete_index.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index"
```

### 四、向量数据操作

#### 12. 插入/更新向量

**方式 1：命令行传入 JSON**
```bash
python3 scripts/put_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --vectors '[{"key":"doc-001","data":{"float32":[0.1,0.2,0.3]},"metadata":{"title":"文档1","category":"AI"}}]'
```

**方式 2：通过文件传入**
```bash
# 准备 vectors.json 文件
cat > vectors.json << 'EOF'
[
  {
    "key": "doc-001",
    "data": {"float32": [0.1, 0.2, 0.3]},
    "metadata": {"title": "人工智能简介", "category": "AI"}
  },
  {
    "key": "doc-002",
    "data": {"float32": [0.4, 0.5, 0.6]},
    "metadata": {"title": "机器学习算法", "category": "AI"}
  }
]
EOF

python3 scripts/put_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --vectors-file vectors.json
```

#### 13. 获取指定向量

```bash
python3 scripts/get_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --keys "doc-001,doc-002" \
  --return-data \
  --return-metadata
```

#### 14. 列出向量列表

```bash
python3 scripts/list_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --max-results 10 \
  --return-metadata
```

#### 15. 删除向量

```bash
python3 scripts/delete_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --keys "doc-001,doc-002"
```

#### 16. 相似度搜索 🔍

这是最核心的能力 —— 根据查询向量找到最相似的 K 个结果。

```bash
python3 scripts/query_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --query-vector '[0.1, 0.2, 0.3]' \
  --top-k 5 \
  --filter '{"category": {"$eq": "AI"}}' \
  --return-distance \
  --return-metadata
```

也可以通过文件传入查询向量：
```bash
python3 scripts/query_vectors.py \
  --region "ap-guangzhou" \
  --bucket "my-vectors-1250000000" \
  --index "my-index" \
  --query-vector-file query.json \
  --top-k 5 \
  --return-distance \
  --return-metadata
```

---

## 🤖 作为 CodeBuddy Skill 使用

这个仓库可以直接作为 [CodeBuddy](https://www.codebuddy.ai/) 的 AI Skill 使用，让 AI 助手自动调用向量桶操作。

### 安装方式

#### 方式 1：全局安装（所有项目可用）

```bash
# 克隆到 CodeBuddy 全局 skill 目录
git clone https://git.woa.com/jimmyyan/cos-vector-skill.git ~/.codebuddy/skills/cos-vector-bucket
```

#### 方式 2：项目级安装（仅当前项目可用）

```bash
# 在项目根目录下执行
git clone https://git.woa.com/jimmyyan/cos-vector-skill.git .codebuddy/skills/cos-vector-bucket
```

#### 方式 3：Git 子模块（推荐团队协作）

```bash
# 添加为子模块
git submodule add https://git.woa.com/jimmyyan/cos-vector-skill.git .codebuddy/skills/cos-vector-bucket
git commit -m "feat: 添加 COS 向量桶 skill"
```

### 使用方式

安装后，在 CodeBuddy 对话中使用自然语言即可触发：

| 你说 | AI 自动执行 |
|------|------------|
| "帮我创建一个向量桶" | 调用 `create_vector_bucket.py` |
| "创建一个 128 维的向量索引" | 调用 `create_index.py` |
| "插入 5 条测试向量数据" | 调用 `put_vectors.py` |
| "列出所有向量数据" | 调用 `list_vectors.py` |
| "搜索和这段文本最相似的向量" | 调用 `query_vectors.py` |
| "删除 demo-index 索引" | 调用 `delete_index.py` |

### Skill 触发关键词

以下关键词会自动触发 skill 加载：

`vector bucket` · `vector index` · `vector search` · `向量桶` · `向量索引` · `向量搜索` · `向量存储` · `插入向量` · `相似度搜索` · `COS vector`

---

## 🏗️ 项目结构

```
cos-vector-skill/
├── README.md                              # 使用文档（本文件）
├── SKILL.md                               # CodeBuddy Skill 定义文件
├── scripts/                               # 可执行脚本目录
│   ├── common.py                          # 公共模块（凭证、客户端、错误处理）
│   ├── create_vector_bucket.py            # 创建向量桶
│   ├── delete_vector_bucket.py            # 删除向量桶
│   ├── get_vector_bucket.py               # 查询向量桶信息
│   ├── list_vector_buckets.py             # 列出所有向量桶
│   ├── put_vector_bucket_policy.py        # 设置桶策略
│   ├── get_vector_bucket_policy.py        # 获取桶策略
│   ├── delete_vector_bucket_policy.py     # 删除桶策略
│   ├── create_index.py                    # 创建向量索引
│   ├── get_index.py                       # 查询索引信息
│   ├── list_indexes.py                    # 列出所有索引
│   ├── delete_index.py                    # 删除向量索引
│   ├── put_vectors.py                     # 插入/更新向量数据
│   ├── get_vectors.py                     # 获取指定向量
│   ├── list_vectors.py                    # 列出向量列表
│   ├── delete_vectors.py                  # 删除向量
│   └── query_vectors.py                   # 相似度搜索
└── references/
    └── api_reference.md                   # API 参考文档
```

---

## 🔧 技术细节

| 配置项 | 说明 |
|--------|------|
| **专用客户端** | 使用 `CosVectorsClient`，不同于普通的 `CosS3Client` |
| **Endpoint** | `vectors.<Region>.coslake.com`，SDK 自动拼接 bucket 前缀 |
| **协议** | 默认 `http`，可选 `https` |
| **桶名格式** | `BucketName-APPID`，如 `my-vectors-1250000000` |
| **桶名规则** | 小写字母、数字和中划线 `-`，长度 3-63 字符 |
| **向量维度** | 1 - 4096 |
| **数据类型** | `float32` |
| **距离度量** | `cosine`（余弦相似度）、`euclidean`（欧氏距离） |
| **加密** | 可选 `AES256` 服务端加密 |

### 输出格式

所有脚本统一输出 JSON 格式：

```json
// 成功
{"success": true, "action": "create_index", "bucket": "...", "index": "...", ...}

// 失败
{"success": false, "error": "错误信息", "error_code": "...", "request_id": "..."}
```

### 公共模块 `common.py`

所有脚本共享的公共模块，提供：

| 函数 | 功能 |
|------|------|
| `base_parser()` | 创建包含凭证参数的基础解析器 |
| `create_client()` | 初始化 CosVectorsClient |
| `success_output()` | 统一的成功输出格式 |
| `fail()` | 统一的错误输出格式并退出 |
| `handle_error()` | 统一的异常处理 |
| `run()` | 包装主函数并捕获异常 |

---

## ❓ 常见问题

### Q: SDK 安装失败怎么办？

```bash
pip3 install cos-python-sdk-v5 --upgrade --force-reinstall
```

### Q: 如何验证凭证是否正确？

```bash
python3 scripts/list_vector_buckets.py \
  --secret-id "你的SecretId" \
  --secret-key "你的SecretKey" \
  --region "ap-guangzhou" \
  --bucket "任意桶名-APPID"
```

如果凭证正确，会返回向量桶列表（可能为空）。

### Q: 支持哪些区域？

常用区域：
- `ap-guangzhou` — 广州
- `ap-shanghai` — 上海
- `ap-beijing` — 北京
- `ap-chengdu` — 成都
- `ap-chongqing` — 重庆

更多区域请参考 [腾讯云 COS 区域列表](https://cloud.tencent.com/document/product/436/6224)。

### Q: 调用失败时如何排查？

1. 检查凭证是否正确
2. 检查 Region 是否正确
3. 检查 Bucket 名称格式是否为 `BucketName-APPID`
4. 检查网络是否能访问 `vectors.<Region>.coslake.com`
5. 查看返回的 `error_code` 和 `request_id` 信息

---

## 📚 参考链接

- [腾讯云 COS 向量数据库官方文档](https://cloud.tencent.com/document/product/436/127755)
- [cos-python-sdk-v5 GitHub](https://github.com/tencentyun/cos-python-sdk-v5)
- [腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)
- [CodeBuddy 官网](https://www.codebuddy.ai/)

---

## 📄 License

MIT
