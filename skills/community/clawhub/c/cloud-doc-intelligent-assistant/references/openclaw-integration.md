# 接入说明

## 设计原则

本 skill 只负责数据采集：
- 从云厂商 API 抓取文档原始内容
- 存储到本地 SQLite 数据库
- 检测文档变更并返回 diff

**不调用大模型。** 总结、摘要、对比分析由调用方（客户端大模型）完成。

## Python 调用

```python
from src.skills import DocAssistant

assistant = DocAssistant()

# 1. 用 doc_ref 抓取单篇文档（存入数据库）
result = assistant.fetch_doc(cloud="aliyun", doc_ref="/vpc/product-overview/what-is-vpc")
content = result["machine"]["items"][0]["content"]
# → 调用方拿到 content 后自行总结

# 2. 从本地数据库查询已存储的文档
result = assistant.fetch_doc(cloud="aliyun", product="vpc")
docs = result["machine"]["items"]  # 每个 item 包含 title, url, content

# 3. 检测变更（需先抓取过文档建立基线）
result = assistant.check_changes(cloud="aliyun", product="vpc", days=7)
changes = result["machine"]["changes"]  # 每个 change 包含 diff
# → 调用方根据 diff 生成变更摘要

# 4. 获取两侧文档供对比
result = assistant.compare_docs(
    left={"cloud": "aliyun", "doc_ref": "/vpc/product-overview/what-is-vpc"},
    right={"cloud": "tencent", "doc_ref": "215/20046"},
    focus="能力差异"
)
left_content = result["machine"]["left"]["content"]
right_content = result["machine"]["right"]["content"]
# → 调用方拿到两侧 content 后自行对比分析

# 5. 文档 diff
result = assistant.summarize_diff(
    title="VPC 文档",
    old_content="旧版本...",
    new_content="新版本..."
)
diff = result["machine"]["diff"]
change_type = result["machine"]["change_type"]  # minor/major/structural
# → 调用方根据 diff 生成摘要

# 6. 批量巡检 + 通知
result = assistant.run_monitor(
    clouds=["aliyun", "tencent", "baidu", "volcano"],
    products=["vpc"],
    send_notification=True
)
```

## CLI 调用

```bash
cloud-doc-skill fetch_doc '{"cloud": "baidu", "doc_ref": "VPC/qjwvyu0at"}'
cloud-doc-skill check_changes '{"cloud": "aliyun", "product": "vpc", "days": 7}'
cloud-doc-skill compare_docs '{"left": {"cloud": "aliyun", "doc_ref": "/vpc/product-overview/what-is-vpc"}, "right": {"cloud": "tencent", "doc_ref": "215/20046"}}'
cloud-doc-skill run_monitor '{"clouds": ["aliyun", "tencent"], "products": ["vpc"], "send_notification": true}'
```

## 返回结构

所有 skill 返回统一的 JSON：

```json
{
  "machine": { ... },
  "human": { "summary_text": "..." },
  "error": null
}
```

- `machine`：结构化数据（文档内容、变更列表、diff 等），供程序读取
- `human`：简短的人类可读文本
- `error`：正常为 `null`，出错时包含 `code`（MISSING_PARAM / INVALID_PARAM / CRAWL_FAILED）和 `message`

## 典型工作流

### 场景一：用户问"阿里云 VPC 是什么"

```
1. fetch_doc(cloud="aliyun", doc_ref="/vpc/product-overview/what-is-vpc")
2. 拿到 content → 调用方大模型总结回答
```

### 场景二：用户问"对比阿里云和腾讯云的 VPC"

```
1. compare_docs(left={...}, right={...})
2. 拿到两侧 content → 调用方大模型对比分析
```

### 场景三：用户问"最近 VPC 文档有什么变化"

```
1. check_changes(cloud="aliyun", product="vpc", days=7)
2. 拿到 changes 列表和 diff → 调用方大模型生成变更摘要
```

### 场景四：定时巡检

```
1. 浏览器收集各云文档 URL
2. fetch_doc 逐篇抓取（建立基线）
3. check_changes 检测变更
4. 调用方大模型生成报告
5. run_monitor 发送通知
```
