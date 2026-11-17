# 三端归档指南

> 每次定时任务运行后，简报必须同步归档到三个位置。
> 归档格式统一为 Markdown + 元数据头。任一端失败只记录日志不中断主流程。

---

## 归档目标

| # | 目标 | 格式 | 路径示例 |
|---|------|------|---------|
| 1 | 飞书云盘 | Markdown 文件（lark-drive 上传） | ClawHub Daily/2026-07-11.md |
| 2 | Obsidian inbox | 本地 .md 文件 | D:/Obsidian/Inbox/clawhub-daily-2026-07-11.md |
| 3 | IMA知识库 | 笔记 + 添加到知识库（两步API） | FIM知识库 / ClawHub Daily |

---

## 元数据头格式

每份归档文件开头必须包含元数据头：

```markdown
---
task_name: "<任务名>"
run_time: "<YYYY-MM-DD HH:MM:SS>"
data_source: "<数据源>"
status: "<success/partial/failed>"
error_count: <N>
archived_to: ["feishu_drive", "obsidian", "ima"]
---

# <简报标题>
<简报正文>
```

**元数据头模板见 [`assets/metadata_header.md`](../assets/metadata_header.md)**

---

## 1. 飞书云盘归档

### 方法
使用 lark-drive skill 的 `drive +upload` 命令上传 Markdown 文件。

### 步骤
1. 确认目标文件夹存在（folder_token）
2. 生成简报 Markdown 文件到临时路径
3. 上传到飞书云盘指定文件夹
4. 记录返回的 file_token

### 脚本调用
```python
import subprocess
result = subprocess.run([
    "python", "-m", "lark_cli", "drive", "upload",
    "--file", "<local_md_path>",
    "--folder-token", "<folder_token>",
    "--name", f"<task-name>-<date>.md"
], capture_output=True, text=True)
```

### 注意事项
- 文件名含日期，确保幂等性（同日重跑覆盖）
- 上传前检查文件大小 > 0
- 上传失败记录日志，不中断主流程

---

## 2. Obsidian Inbox 归档

### 方法
直接写入本地文件系统。

### 步骤
1. 确认 inbox 目录存在（不存在则创建）
2. 生成简报 Markdown 内容
3. 写入 `<inbox_path>/<task-name>-<date>.md`

### 脚本调用
```python
import os
from pathlib import Path
from datetime import datetime

inbox_path = Path(os.environ.get("OBSIDIAN_INBOX", "<obsidian_inbox_path>"))
inbox_path.mkdir(parents=True, exist_ok=True)

date_str = datetime.now().strftime("%Y-%m-%d")
file_path = inbox_path / f"<task-name>-{date_str}.md"
file_path.write_text(content, encoding="utf-8")
```

### 注意事项
- 默认 inbox 路径: `D:/Obsidian/Inbox`
- 文件名格式: `<task-name>-<date>.md`
- 同日重跑覆盖（幂等性）
- 编码必须 UTF-8

---

## 3. IMA知识库归档

### 方法
两步API流程（**不能用 note API 的 folder 参数**）：
1. `POST /openapi/note/v1/import_doc` — 创建笔记
2. `POST /openapi/wiki/v1/add_knowledge` — 添加到知识库

### 凭证
```python
import os
client_id = os.environ.get("IMA_OPENAPI_CLIENTID") or os.environ.get("IMA_CLIENT_ID")
api_key = os.environ.get("IMA_OPENAPI_APIKEY") or os.environ.get("IMA_API_KEY")
```

### Step 1: 创建笔记
```python
import urllib.request, json

url = "https://api.imawiki.com/openapi/note/v1/import_doc"
data = json.dumps({
    "title": f"<task-name>-<date>",
    "content": briefing_content,  # Markdown 内容
    "source": "cron-task"
}).encode("utf-8")

req = urllib.Request(url, data=data, headers={
    "Content-Type": "application/json",
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key
})
resp = urllib.request.urlopen(req)
note_id = json.loads(resp.read())["data"]["note_id"]
```

### Step 2: 添加到知识库
```python
kb_id = os.environ.get("IMA_KB_ID", "<ima_kb_id>")  # FIM知识库

url = "https://api.imawiki.com/openapi/wiki/v1/add_knowledge"
data = json.dumps({
    "kb_id": kb_id,
    "media_type": 11,
    "note_info": {"content_id": note_id}
}).encode("utf-8")

req = urllib.Request(url, data=data, headers={
    "Content-Type": "application/json",
    "ima-openapi-clientid": client_id,
    "ima-openapi-apikey": api_key
})
resp = urllib.request.urlopen(req)
```

### 注意事项
- **两套API不可混用**：Notes API 管笔记，Knowledge Base API 管知识库
- **folder_id ≠ knowledge_base_id**：必须用 get_knowledge_list 获取 folder_id
- **X/Twitter链接不用import_urls**：用 create_note + add_knowledge 纯文本笔记
- 凭证环境变量双兼容：优先 `IMA_OPENAPI_*`，回退 `IMA_*`

---

## 归档失败处理

| 失败端 | 处理方式 | 是否中断主流程 |
|--------|---------|--------------|
| 飞书云盘 | 记录错误日志，继续其他端归档 | 否 |
| Obsidian | 记录错误日志，继续其他端归档 | 否 |
| IMA | 记录错误日志，继续其他端归档 | 否 |
| 三端全失败 | 记录错误日志，IM提醒中标注归档失败 | 否 |

### 错误日志格式
```python
import logging
logging.basicConfig(filename="logs/archive-<date>.log", level=logging.ERROR)
logging.error(f"[{target}] {error_type}: {error_message}")
```

---

## 归档验证

归档完成后，验证三端可达性：

```python
def verify_archive(feishu_file_token, obsidian_path, ima_note_id):
    results = {}
    
    # 飞书云盘验证
    results["feishu"] = bool(feishu_file_token)
    
    # Obsidian验证
    results["obsidian"] = Path(obsidian_path).exists()
    
    # IMA验证
    results["ima"] = bool(ima_note_id)
    
    return results
```

验证结果写入元数据头的 `archived_to` 字段。
