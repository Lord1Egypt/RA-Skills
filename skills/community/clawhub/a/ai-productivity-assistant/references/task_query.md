# 任务查询接口

查询视频/图片生成任务的状态和结果。

## 本地接口列表

| 接口 | 说明 |
|-----|------|
| `GET  /api/task/{task_id}` | 查询单个任务 |
| `POST /api/tasks/query` | 批量查询多个任务 |
| `GET  /api/tasks` | 查询本地任务列表 |
| `GET  /api/status` | 检查客户端状态 |

---

## 1. 查询单个任务

`GET http://127.0.0.1:17321/api/task/{task_id}`

### 响应参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| success | bool | 请求是否成功 |
| id | string | 任务 ID |
| object | string | 类型：`video` 或 `image` |
| model | string | 使用的模型 |
| status | string | 任务状态（见下方状态说明） |
| progress | number | 进度 0-100 |
| created_at | number | 创建时间戳（秒） |
| completed_at | number | 完成时间戳（秒，仅 completed 状态返回） |
| url | string | 结果 URL（仅 completed 状态返回） |
| error | string | 错误信息（仅 failed 状态返回） |

### 任务状态说明

| status | 说明 |
|--------|------|
| `queued` | 排队中，等待处理 |
| `processing` | 处理中，AI 正在生成 |
| `completed` | 已完成，url 字段包含结果 |
| `failed` | 失败，error 字段包含原因 |
| `timeout` | 等待超时（本地超时，任务仍在运行） |

### 示例

```python
from local_client import get_client
client = get_client()

# 查询任务状态
task = client.query_task("task_xxxxxxxxxxxxx")
print(task["status"])    # completed
print(task["url"])       # https://example.com/result.mp4

# 等待完成（自动轮询，每 5 秒一次）
final = client.wait_for_result("task_xxxxxxxxxxxxx", timeout=600)
if final["status"] == "completed":
    print(f"✅ 完成: {final['url']}")
elif final["status"] == "failed":
    print(f"❌ 失败: {final['error']}")
elif final["status"] == "timeout":
    print(f"⏱️ 超时，task_id: task_xxxxxxxxxxxxx，可稍后继续查询")
```

---

## 2. 批量查询多个任务

`POST http://127.0.0.1:17321/api/tasks/query`

### 请求体

```json
{
    "task_ids": ["task_001", "task_002", "task_003"]
}
```

### 响应示例

```json
{
    "success": true,
    "results": [
        {
            "task_id": "task_001",
            "success": true,
            "status": "completed",
            "progress": 100,
            "url": "https://example.com/video1.mp4"
        },
        {
            "task_id": "task_002",
            "success": true,
            "status": "processing",
            "progress": 60
        },
        {
            "task_id": "task_003",
            "success": true,
            "status": "failed",
            "error": "内容违规"
        }
    ]
}
```

### 示例

```python
# 批量查询（一次性快照，不等待）
result = client.query_tasks(["task_001", "task_002", "task_003"])
for t in result["results"]:
    print(f"{t['task_id']}: {t['status']}")

# 并发等待所有任务完成（推荐）
finals = client.wait_for_results(
    ["task_001", "task_002", "task_003"],
    timeout=600,
    on_progress=lambda tid, status, progress: print(f"{tid}: {status} {progress}%")
)

for f in finals:
    if f["status"] == "completed":
        print(f"✅ {f.get('id', f.get('task_id'))}: {f['url']}")
    else:
        print(f"❌ {f.get('id', f.get('task_id'))}: {f.get('error', f['status'])}")
```

---

## 3. 查询本地任务列表

`GET http://127.0.0.1:17321/api/tasks`

### 查询参数

| 参数 | 说明 |
|-----|------|
| status | 可选，过滤状态：`queued` / `processing` / `completed` / `failed` |

### 示例

```python
# 查询最近 50 条任务
all_tasks = client.list_tasks()
print(f"共 {len(all_tasks['tasks'])} 条任务")

# 查询进行中的任务
processing = client.list_tasks(status="processing")

# 查询已完成的任务
completed = client.list_tasks(status="completed")
for t in completed["tasks"]:
    print(f"{t['id']}: {t.get('url', '')}")
```

---

## 4. 检查客户端状态

`GET http://127.0.0.1:17321/api/status`

### 响应示例

```json
{
    "success": true,
    "running": true,
    "version": "1.0.0",
    "gateway": "https://your-gateway.com",
    "ready": true
}
```

| 字段 | 说明 |
|-----|------|
| running | 客户端是否在运行 |
| ready | 是否已配置网关（SK），可以生成 |
| version | 客户端版本号 |
| gateway | 当前配置的网关地址 |

### 示例

```python
status = client.status()
if not status.get("ready"):
    print("⚠️ 客户端未配置 SK，请先在客户端完成配置")
else:
    print(f"✅ 客户端就绪，版本: {status['version']}")
```

---

## 完整批量生成并查询示例

```python
from local_client import get_client

client = get_client()

# 1. 检查客户端
client.check_client()

# 2. 批量提交
tasks = [
    {"model": "sora-2-landscape-10s", "prompt": "春天樱花飘落"},
    {"model": "sora-2-landscape-10s", "prompt": "夏日海浪拍岸"},
    {"model": "nano_banana_2", "prompt": "秋天枫叶特写", "metadata": {"aspectRatio": "16:9", "urls": []}},
]

batch = client.generate_batch(tasks)
print(f"✅ 已提交 {len(batch['results'])} 个任务")

# 3. 提取成功提交的 task_id
task_ids = []
for r in batch["results"]:
    if r.get("success"):
        task_ids.append(r["task_id"])
        print(f"  - {r['task_id']} ({r['model']})")
    else:
        print(f"  - ❌ 提交失败: {r.get('error')}")

# 4. 并发等待所有任务完成
print("\n⏳ 等待生成完成...")
finals = client.wait_for_results(
    task_ids,
    timeout=600,
    on_progress=lambda tid, s, p: print(f"  {tid[:16]}... {s} {p}%")
)

# 5. 展示结果
print("\n📋 生成结果：")
for i, f in enumerate(finals):
    if f["status"] == "completed":
        obj_type = f.get("object", "unknown")
        url = f["url"]
        if obj_type == "image":
            print(f"  图片{i+1}: ![image]({url})")
        else:
            print(f"  视频{i+1}: [点击查看]({url})")
    elif f["status"] == "failed":
        print(f"  任务{i+1}: ❌ {f.get('error', '未知错误')}")
    elif f["status"] == "timeout":
        print(f"  任务{i+1}: ⏱️ 超时，task_id={f['task_id']}，可稍后查询")
```
