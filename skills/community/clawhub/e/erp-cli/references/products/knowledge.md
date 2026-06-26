# 知识库（knowledge）产品参考

RAGFlow 知识库检索——**所有非 ERP 操作的问题默认先搜知识库**。

## 核心原则

**知识库优先**：99% 的问题先过知识库，搜到结合原文回答，搜不到 AI 用通用知识回答。只有明确要**操作 ERP 系统**（查数据、建工单、分派、接单）才走 ERP Shortcut。

## 意图判断

| 用户说... | 判断 | 命令 |
|-----------|------|------|
| "报修流程是什么" | 问制度，非 ERP 操作 | `knowledge +search` |
| "帮我建个报修工单" | 要操作 ERP | `workorder +create` |
| "消防巡检不合格怎么处理" | 问规范，非 ERP 操作 | `knowledge +search` |
| "我的待办工单" | 查 ERP 数据 | `workorder +list` |
| "分派工单给张三" | 操作 ERP | `workorder +apportion` |
| "物业费收费标准" | 问标准，非 ERP 操作 | `knowledge +search` |
| "电梯困人怎么办" | 问应急，非 ERP 操作 | `knowledge +search` |
| "今天午饭吃什么" | 闲聊 | `knowledge +search`（搜不到 AI 自己回答） |

**判断原则**：用户要**增删改查 ERP 系统里的数据** → ERP Shortcut；其他 → `knowledge +search`。

---

## +check — 检查 RAGFlow 连通性 ✅

不需要 ERP 登录，不需要 API Key。

```bash
erp-cli --as me knowledge +check
```

**输出**：
```json
{"ok": true, "data": {"healthy": true, "status": "ok", "db": "ok", "redis": "ok", "docEngine": "ok", "storage": "ok"}}
```

---

## +list-datasets — 列出知识库 ✅

首次配置时用——查看有哪些知识库，把 ID 填入 config 的 `ragflow.defaultDatasetIds`。

```bash
erp-cli --as me knowledge +list-datasets
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--page` | 否 | 页码（默认 1） |
| `--page-size` | 否 | 每页条数（默认 30） |

**输出**：
```json
{
  "ok": true,
  "data": {
    "total": 1,
    "datasets": [
      {
        "id": "cd018c845b4011f185a93582a7bd31ea",
        "name": "物业管理制度",
        "documentCount": 15,
        "chunkCount": 59,
        "embeddingModel": "BAAI/bge-large-zh-v1.5"
      }
    ]
  }
}
```

---

## +search — 检索知识库 ✅

**核心高频命令**。所有非 ERP 操作的问题都走这个。

```bash
# 最常见用法（用 config 里的 defaultDatasetIds）
erp-cli --as me knowledge +search --question "消防巡检不合格怎么处理"

# 指定知识库
erp-cli --as me knowledge +search --question "消防巡检" --dataset-ids id1,id2

# 调整检索精度
erp-cli --as me knowledge +search --question "消防巡检" --similarity-threshold 0.5 --page-size 10
```

**参数**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--question` | 是 | 检索问题 |
| `--dataset-ids` | 否 | 知识库 ID 逗号分隔（空=用 config 中的 `ragflow.defaultDatasetIds`） |
| `--page` | 否 | 页码（默认 1） |
| `--page-size` | 否 | 每页返回 chunks 数（默认 6） |
| `--similarity-threshold` | 否 | 最低相似度（默认 0.2，越高越严格） |
| `--vector-similarity-weight` | 否 | 向量相似度权重（默认 0.3，1-此值=词频权重） |

**不需要 ERP 登录**。知识库检索走 RAGFlow API Key，跟 ERP token 无关。

**输出**（搜到时）：
```json
{
  "ok": true,
  "data": {
    "total": 3,
    "chunks": [
      {
        "content": "消防巡检不合格时，应在24小时内整改并提交整改报告...",
        "documentName": "消防巡检制度.pdf",
        "similarity": 0.87,
        "datasetId": "8e83e57a884611ef9d760242ac120006"
      }
    ]
  }
}
```

**输出**（搜不到时）：
```json
{
  "ok": true,
  "data": {
    "total": 0,
    "chunks": [],
    "hint": "知识库中未找到相关内容，AI 可用通用知识回答，但建议告知用户此回答未引用知识库"
  }
}
```

---

## AI 行为规则

### 必须遵守

1. **所有非 ERP 操作的问题，先调 `knowledge +search`**——这是默认路径，不是可选路径
2. **搜到时**：基于 chunks 内容回答，标注来源文档名（如"根据《消防巡检制度.pdf》..."）
3. **搜不到时**：可以用 AI 通用知识回答，但必须告知用户"此回答未引用知识库，仅供参考"
4. **不要跳过知识库**——即使 AI 觉得自己知道答案，也要先搜。知识库内容可能比 AI 训练数据更新、更准确
5. **相似度低时**：chunks 最高相似度 < 0.4，提醒用户"匹配度较低，以下回答仅供参考"

### 可以灵活处理

1. **多轮追问**：同一话题后续问题，可复用上一轮 chunks，不重复调 `+search`
2. **纯闲聊**（"你好"、"谢谢"）：可以不搜知识库，直接回答

### 错误处理

1. **RAGFlow 未配置（缺 URL / API Key / Dataset IDs）**：**主动帮用户配置**，执行 `erp-cli --as <身份> config ragflow`，让命令交互式引导用户输入 URL、API Key，并自动列出知识库让用户选择。**不要自行填入配置值，必须让用户通过交互式命令自己提供**
2. **RAGFlow 不可达**：AI 降级为通用知识回答，告知用户"知识库服务暂时不可用"
3. **ERP 未登录不影响知识库**：`+search` 不依赖 ERP token

**知识库未配置时的 AI 行为**：
```
1. 用户提问 → AI 调 knowledge +search
2. 返回错误：RAGFlow 未配置（缺 ragflow.baseUrl / ragflow.apiKey / ragflow.defaultDatasetIds）
3. AI 告知用户："知识库尚未配置，我来帮你设置，需要你提供 RAGFlow 信息"
4. AI 执行：erp-cli --as <身份> config ragflow
5. 命令会交互式引导用户输入 URL、API Key，并自动列出知识库让用户选择
6. 配置完成后，AI 重新执行 knowledge +search 回答用户问题
```

---

## 配置

### config ragflow — 交互式配置知识库

一条命令完成 RAGFlow 所有配置，**AI 发现知识库未配置时应执行此命令让用户交互式填写**：

```bash
erp-cli --as me config ragflow
```

交互流程：
```
RAGFlow URL [http://223.80.101.21:39054]: ← 回车用默认，或输入新地址
RAGFlow API Key: ragflow-VhNmRiYm...     ← 用户输入 API Key
Querying available datasets...

Available datasets:
  1. 物业管理制度 (ID: cd018c845b4011f185a93582a7bd31ea, 15 documents)
  2. 消防应急预案 (ID: ab123..., 8 documents)

Dataset IDs (comma-separated): cd018c845b4011f185a93582a7bd31ea

RAGFlow configuration saved.
  Base URL:  http://223.80.101.21:39054
  API Key:   ragflow-Vh...
  Datasets:  cd018c845b4011f185a93582a7bd31ea

Verify with: erp-cli --as me knowledge +check
```

### 手动逐项配置

如需逐项设置，用 `config set`：

```bash
erp-cli --as me config set ragflow.baseUrl http://223.80.101.21:39054
erp-cli --as me config set ragflow.apiKey ragflow-xxxxxxxx
erp-cli --as me config set ragflow.defaultDatasetIds '["id1","id2"]'
```

### 配置文件

RAGFlow 配置存储在 `~/.erp-cli/config.json` 的 `ragflow` 段：

```json
{
  "ragflow": {
    "baseUrl": "http://223.80.101.21:39054",
    "apiKey": "ragflow-xxxxxxxx",
    "defaultDatasetIds": ["cd018c845b4011f185a93582a7bd31ea"]
  }
}
```

| 字段 | 说明 |
|------|------|
| `baseUrl` | RAGFlow 服务地址 |
| `apiKey` | RAGFlow API Key（永不过期） |
| `defaultDatasetIds` | `+search` 默认检索的知识库 ID 列表 |