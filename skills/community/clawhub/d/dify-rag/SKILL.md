---
name: "dify-rag"
description: "Dify.AI 知识库只读检索：检索共享知识库供其他 skill 调用；无上传/变更操作，内容由用户在 Dify 控制台管理"
user-invocable: true
allowed-tools:
  - exec
  - read
  - memory_search
---

# Dify.AI 知识库只读检索

通过 Dify.ai 知识库 API 检索跨 OpenClaw 实例共享的研发知识库。

**只读边界**：本 skill 不包含任何上传、修改、删除操作。知识库内容的增删改统一由用户登录 Dify 控制台手动管理（2026-11-10 决定）。原"上传文档/批量导入"能力已移除。

## 设计定位

本 skill 是其他 skill 的**公共检索层**：tech-research / prd-generator / tech-doc / git-summary 需要检索知识库时，统一调用本 skill，不直接拼 Dify API。

## 配置

从 `workspace/TOOLS.md` 的「Dify.AI RAG 配置」段读取（其次环境变量）：

| 参数 | 说明 | 示例 |
|------|------|------|
| `DIFY_API_BASE` | API 地址 | `https://api.dify.ai` |
| `DIFY_API_KEY` | 知识库 API 密钥（`dataset-` 开头，完整 32+ 字符） | 见 TOOLS.md |
| `DIFY_DATASET_ID` | 知识库 ID（UUID） | 从 Dify 知识库页面 URL 的 `/datasets/<id>` 部分复制 |

> **密钥访问范围**：密钥创建时可限定只访问部分知识库（创建后不可改）。限定范围的密钥调用"获取知识库列表"（`GET /v1/datasets`）等不指定知识库的接口会返回 403，属正常现象（2026-11-10 实测确认）；对已授权知识库的检索不受影响。
>
> **密钥保真**：密钥含完整 `dataset-` 前缀与 32 位主体，任何配置/命令中出现 `datase…NxcP` 这类省略号形式均为脱敏显示，**不能作为实际值调用**（会得到无效请求）。写入或传递密钥时必须使用完整字面量，可用字符串长度 + ASCII 校验确认。

## 检索方式

### 方式一：检索脚本（推荐）

```bash
python {baseDir}/scripts/search.py --query "WebRTC 弱网自适应" --top-k 5
```

`{baseDir}` 为本 skill 安装目录（OpenClaw 加载时自动解析），无需关心实际安装位置。

| 参数 | 说明 |
|------|------|
| `--query` | 必填，检索问题，最长 250 字符（超长自动截断并提示） |
| `--top-k` | 返回条数，默认 5 |
| `--score-threshold` | 相似度阈值（如 0.5），提供则启用阈值过滤 |
| `--search-method` | `semantic_search`（默认）/ `full_text_search` / `hybrid_search` |
| `--json` | 输出原始 JSON（供程序化解析） |
| `--api-base` / `--api-key` / `--dataset-id` | 覆盖环境配置 |

脚本无第三方依赖（仅 Python 标准库），配置来源优先级：命令行参数 > 环境变量。

### 方式二：直接 curl（脚本不可用时）

```bash
curl -s -X POST "$DIFY_API_BASE/v1/datasets/$DIFY_DATASET_ID/retrieve" \
  -H "Authorization: Bearer $DIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"<关键词>","retrieval_model":{"top_k":5,"search_method":"semantic_search","reranking_enable":false,"score_threshold_enabled":false}}'
```

> **retrieval_model 必填字段**：`reranking_enable` 和 `score_threshold_enabled` 缺一不可（2026-11-10 实测，缺失返回 400 invalid_param HitTestingPayload）。脚本已内置。
>
> Windows PowerShell 下变量引用改用 `$env:DIFY_API_KEY` 形式；JSON body 含双引号时建议用 `--%` 停止解析符或写入临时文件后 `-d @file`。

## 响应结构（2025+ 版 API，2026-11-10 实测验证）

结果在 `records[]` 数组中，字段**嵌套在 `segment` 下**：

- `records[].segment.content` — 分段内容（主要取这里）
- `records[].segment.document.name` — 来源文档名
- `records[].segment.position` — 段落在文档中的位置
- `records[].score` — 相关性分数
- `records[].child_chunks` — 子分段（父子分段模式的知识库）

> 注意：旧版接口直接返回 `records[].content`，新版已嵌套。解析逻辑以 `records[].segment.content` 为准；结构存疑时先用 `--json` 确认实际返回。

## 其他 skill 的调用约定

1. 定位本 skill 安装目录：默认 `skills/dify-rag/`（相对 workspace）；若不确定，先确认 dify-rag 的实际路径
2. `exec` 执行 `python <dify-rag安装目录>/scripts/search.py --query "<关键词>" --top-k 5`
3. 读取格式化输出（已含序号、分数、来源文档名、内容）
4. 需要程序化处理时加 `--json`

## 故障排查

| 现象 | 原因与处理 |
|------|-----------|
| 403 forbidden | ① 密钥访问范围不含该知识库；② 该知识库关闭了「访问 API」开关；③ 限定范围密钥调用了不指定知识库的接口（正常）→ 由用户在 Dify 控制台检查 |
| 401 unauthorized | 密钥无效或已被删除 → 用户重新生成密钥并更新 TOOLS.md |
| 400 invalid_param | retrieval_model 缺必填字段（reranking_enable / score_threshold_enabled）→ 用脚本检索或补全字段 |
| 404 | Dataset ID 不存在或拼写错误 → 核对知识库 URL 中 `/datasets/<id>` |
| 429 / 频率限制 | Dify Cloud 有请求频率限制 → 退避重试 |
| 超时/连接失败 | 检查网络与 API 地址（自部署实例确认地址） |

**降级策略**：Dify 不可用时改用本地 `memory_search`，并在回复中注明结果来自本地记忆而非共享知识库。

## 注意事项

- API Key 只存在 TOOLS.md 或环境变量中，**绝不写入 SKILL.md 或任何对外分享/上传的文件**
- `economy` 索引方式的知识库只支持关键词检索，`search_method` 会被忽略
- query 上限 250 字符，长问题先拆分关键词分次检索
- 接口文档：https://docs.dify.ai/zh/api-reference/guides/knowledge
