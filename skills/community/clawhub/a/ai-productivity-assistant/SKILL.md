---
name: AI 生产力工具助手
description: |
  批量生成视频图片客户端助手，可以通过对话驱动本地客户端生成视频和图片。
  支持对接飞书、QQ、微信等对话入口，不用再限制在电脑前使用，随时随地都可以生成。

  当用户提到以下意图时使用此技能：
  「生成视频」「生成图片」「文生视频」「图生视频」「文生图」「图生图」
  「Sora 生成」「Veo 生成」「Nano Banana 生成」「批量生成」
  「查任务」「查进度」「查结果」「任务状态」
  「检查客户端」「客户端状态」

  支持：文生视频、图生视频（首尾帧/参考图）、文生图、图生图，
  支持单个生成和批量生成，所有请求发往本机客户端 http://127.0.0.1:17321，
  无需任何 API Key，只需保持 DYU 客户端在运行。
version: 1.0.0
author: dyu
metadata: { "openclaw": { "requires": { "python": [ "requests>=2.31.0" ] }, "primaryEnv": "", "requiredEnv": [], "optionalEnv": [], "homepage": "", "securityNotes": "本技能仅通过本机 127.0.0.1:17321 与已运行的本地客户端通信；外部网关/代理等网络访问均由客户端自身配置与路由决定，Skill 不硬编码任何外部网址/域名，也不需要配置凭证。" } }
---

# AI 生产力工具助手

## 一、必读约束

### 工作原理

本技能与**本地已安装的视频/图片批量生成客户端**通信，无需 API Key，无需配置凭证。

```
你（对话） → OpenClaw Skill → http://127.0.0.1:17321 → 本地批量生成客户端 → AI 生成服务
```

### 前置条件

**本地批量生成客户端必须处于运行状态**，且已完成 SK 配置。每次执行任务前，先调用 `scripts/local_client.py` 中的 `check_client()` 确认客户端在线。

### 任务处理规范

1. **提交成功后必须立即返回 `task_id`**，不要在对话里持续轮询刷屏（不要调用 `wait_for_result`）
2. 提交后统一提示用户：**生成结果大概需要 3-10 分钟**，请稍后查询结果
3. 给出“一键复制”的查询指令：**必须单独放在一个 `text` 代码块中**（便于用户点击复制）
   - 示例：
     ```text
     查询任务 task_xxxxxxxxxxxxx
     ```
4. 只有当用户明确要求「查询进度 / 查询结果 / 等结果」时，才调用查询接口：
   - 默认只查询 **一次**：`GET /api/task/{task_id}`
   - 如用户要求持续跟进，可按用户要求轮询，但要控制频率（建议 5 秒一次）
   - **拿到结果链接时，必须使用 `video_url`（首选）或 `url`，并且原样保留 `?` 之后的全部查询参数**
5. `status = completed` → 将 `url` 字段展示给用户（图片直接渲染，视频给出链接）
6. `status = failed` → 告知用户失败原因，并询问是否重新生成

### 安全约定

- 所有请求只发往 `http://127.0.0.1:17321`，不访问任何外部地址
- 客户端离线时，友好提示用户启动 DYU 客户端

---

## 二、本地接口说明

所有接口均为 `http://127.0.0.1:17321`，调用 `scripts/local_client.py` 封装的客户端。

```python
from local_client import get_client

client = get_client()

# 检查客户端状态
status = client.status()

# 提交单个任务
result = client.generate({ "model": "...", "prompt": "..." })

# 提交批量任务
results = client.generate_batch([
    { "model": "...", "prompt": "..." },
    { "model": "...", "prompt": "..." },
])

# 查询单个任务
task = client.query_task("task_xxxxx")

# 批量查询任务
tasks = client.query_tasks(["task_xxx1", "task_xxx2"])

# （可选）等待任务完成（自动轮询）
final = client.wait_for_result("task_xxxxx", timeout=600)
```

---

## 三、快速决策表

| 用户意图 | 示例说法 | 模型参数 | 备注 |
|---------|---------|---------|------|
| **视频 - Sora** | | | |
| Sora 横屏 10 秒 | "用 Sora 生成横屏视频" | `sora-2-landscape-10s` | 默认横屏选此 |
| Sora 竖屏 10 秒 | "生成竖屏短视频" | `sora-2-portrait-10s` | |
| Sora 横屏 15 秒 | "15 秒横屏视频" | `sora-2-landscape-15s` | |
| Sora 竖屏 15 秒 | "15 秒竖屏视频" | `sora-2-portrait-15s` | |
| Sora Pro 横屏 25 秒 | "25 秒高质量视频" | `sora-2-pro-landscape-25s` | |
| Sora Pro 竖屏 25 秒 | "25 秒竖屏高质量" | `sora-2-pro-portrait-25s` | |
| Sora Pro HD 横屏 15 秒 | "HD 高清横屏视频" | `sora-2-pro-landscape-hd-15s` | |
| Sora Pro HD 竖屏 15 秒 | "HD 高清竖屏视频" | `sora-2-pro-portrait-hd-15s` | |
| Sora 图生视频（URL） | "把这张图做成视频 https://..." | `sora-2-portrait-10s` + `image_url` | |
| **视频 - Veo** | | | |
| Veo 文生视频 | "用 Veo 生成视频" | `veo_3_1-fast` + `size=1920x1080` | 标清/默认 |
| Veo 竖屏 | "Veo 竖屏视频" | `veo_3_1-fast` + `size=1080x1920` | 标清/默认 |
| Veo 高清文生视频 | "用 Veo 生成高清视频"、"Veo 高清 1080P" | `veo_3_1-fast-hd` + `size=1920x1080` | 需在 `/api/pricing` 中已启用 |
| Veo 高清竖屏 | "Veo 高清竖屏视频" | `veo_3_1-fast-hd` + `size=1080x1920` | 需在 `/api/pricing` 中已启用 |
| Veo 首尾帧 | "以这两张图为首尾帧" | `veo_3_1-fast-fl` + `size=1920x1080` | 需要 image_url |
| Veo 高清首尾帧 | "以这两张图为首尾帧生成高清视频" | `veo_3_1-fast-fl-hd` + `size=1920x1080` | 需要 image_url，需在 `/api/pricing` 中已启用 |
| Veo 参考图 | "参考这张图生成视频" | `veo_3_1-fast` + `input_reference` | |
| **图片 - Nano Banana** | | | |
| 标准文生图 | "生成一张图片" | `nano_banana_2` | 默认选此 |
| Pro 文生图 | "生成 Pro 图片" | `nano_banana_pro` | |
| 1K 高清图 | "生成 1K 高清图" | `nano_banana_pro-1K` | |
| 2K 超清图 | "生成 2K 超清图" | `nano_banana_pro-2K` | |
| 4K 极清图 | "生成 4K 极清图" | `nano_banana_pro-4K` | |
| 图生图 | "把这张图转成油画" | `nano_banana_2` + `metadata.urls` | |

---

## 四、意图关键词判断

### 横竖屏判断
| 用户说 | 参数 |
|-------|------|
| 横屏、横版、16:9、landscape | Sora 选 `landscape` 模型；Veo 选 `size=1920x1080` |
| 竖屏、竖版、9:16、portrait | Sora 选 `portrait` 模型；Veo 选 `size=1080x1920` |
| 未指定 | 默认横屏 |

### 时长判断（Sora）
| 用户说 | 模型后缀 |
|-------|---------|
| 10 秒、10s、短视频 | `-10s` |
| 15 秒、15s | `-15s` |
| 25 秒、25s、长视频 | `-25s`（Pro） |
| HD、高清 | `-hd-15s`（Pro HD） |
| 未指定 | 默认 `-10s` |

### 图片分辨率判断（Nano Banana）
| 用户说 | 模型 |
|-------|------|
| 普通、标准、快速 | `nano_banana_2` |
| Pro | `nano_banana_pro` |
| 1K | `nano_banana_pro-1K` |
| 2K | `nano_banana_pro-2K` |
| 4K | `nano_banana_pro-4K` |
| 未指定 | `nano_banana_2` |

### 宽高比判断（图片）
| 用户说 | metadata.aspectRatio |
|-------|---------------------|
| 横图、横版、16:9 | `16:9` |
| 竖图、竖版、9:16 | `9:16` |
| 正方形、1:1 | `1:1` |
| 未指定 | `auto` |

---

## 五、单个生成示例

### 示例 1：Sora 文生视频
```python
from local_client import get_client
client = get_client()

result = client.generate({
    "model": "sora-2-landscape-10s",
    "prompt": "一只可爱的橘猫在阳光明媚的花园里玩耍，镜头缓慢推进"
})
# result = {"success": True, "task_id": "task_xxx", "status": "queued", ...}
# 对话中不要轮询：直接把 task_id 返回给用户，并提示 3-10 分钟后查询：
# 你可以发送：查询任务 task_xxx
```

### 示例 2：Veo 文生视频
```python
result = client.generate({
    "model": "veo_3_1-fast",
    "prompt": "夕阳下的海边，海浪轻轻拍打礁石，光影变幻",
    "size": "1920x1080"
})
# 对话中不要轮询：直接返回 task_id，并提示稍后查询
```

### 示例 3：Sora 图生视频（图片 URL）
```python
result = client.generate({
    "model": "sora-2-portrait-10s",
    "prompt": "让画面动起来，人物微微转头微笑",
    "image_url": "https://example.com/photo.jpg"
})
# 对话中不要轮询：直接返回 task_id，并提示稍后查询
```

### 示例 4：Nano Banana 文生图
```python
result = client.generate({
    "model": "nano_banana_2",
    "prompt": "美丽的日出风景，金色阳光洒在宁静湖面，远处连绵山脉，写实风格",
    "metadata": {
        "aspectRatio": "16:9",
        "urls": []
    }
})
# 对话中不要轮询：直接返回 task_id，并提示 3-10 分钟后查询：
# 你可以发送：查询任务 task_xxx
```

### 示例 5：Nano Banana 图生图
```python
result = client.generate({
    "model": "nano_banana_2",
    "prompt": "将这张图片转换成梵高油画风格，保留主体构图",
    "metadata": {
        "aspectRatio": "1:1",
        "urls": ["https://example.com/reference.jpg"]
    }
})
# 对话中不要轮询：直接返回 task_id，并提示稍后查询
```

---

## 六、批量生成示例

### 示例 6：批量文生视频（Sora，多个提示词）
```python
from local_client import get_client
client = get_client()

tasks = [
    {
        "model": "sora-2-landscape-10s",
        "prompt": "春天的樱花树下，花瓣随风飘落"
    },
    {
        "model": "sora-2-landscape-10s",
        "prompt": "夏日海边，孩子们在沙滩上奔跑嬉戏"
    },
    {
        "model": "sora-2-landscape-10s",
        "prompt": "秋天的枫叶林，金红色叶片在阳光下闪耀"
    },
    {
        "model": "sora-2-landscape-10s",
        "prompt": "冬日雪景，白雪覆盖的山村宁静祥和"
    }
]

# 提交批量任务
batch_result = client.generate_batch(tasks)
# batch_result = {"success": True, "results": [{"task_id": "task_001", ...}, ...]}

# 提取所有 task_id
task_ids = [r["task_id"] for r in batch_result["results"] if r.get("success")]

# 对话中不要轮询：直接返回 task_ids，并提示用户稍后逐个查询：
# 你可以发送：查询任务 task_001
```

### 示例 7：批量文生图（Nano Banana，不同比例）
```python
tasks = [
    {
        "model": "nano_banana_pro-1K",
        "prompt": "产品主图：一款高端智能手表，白色背景，专业摄影",
        "metadata": {"aspectRatio": "1:1", "urls": []}
    },
    {
        "model": "nano_banana_pro-1K",
        "prompt": "产品场景图：智能手表佩戴在手腕上，户外运动场景",
        "metadata": {"aspectRatio": "16:9", "urls": []}
    },
    {
        "model": "nano_banana_pro-1K",
        "prompt": "产品细节图：智能手表表盘特写，展示精致工艺",
        "metadata": {"aspectRatio": "9:16", "urls": []}
    }
]

batch_result = client.generate_batch(tasks)
task_ids = [r["task_id"] for r in batch_result["results"] if r.get("success")]
# 对话中不要轮询：直接返回 task_ids，并提示稍后查询
```

### 示例 8：批量图生图（风格迁移）
```python
reference_images = [
    "https://example.com/photo1.jpg",
    "https://example.com/photo2.jpg",
    "https://example.com/photo3.jpg",
]

tasks = [
    {
        "model": "nano_banana_2",
        "prompt": "转换成水彩画风格，保留原图构图和色调",
        "metadata": {"aspectRatio": "auto", "urls": [img_url]}
    }
    for img_url in reference_images
]

batch_result = client.generate_batch(tasks)
task_ids = [r["task_id"] for r in batch_result["results"] if r.get("success")]
# 对话中不要轮询：直接返回 task_ids，并提示稍后查询
```

### 示例 9：批量 Veo 视频（不同尺寸）
```python
tasks = [
    {
        "model": "veo_3_1-fast",
        "prompt": "城市夜景延时摄影，霓虹灯光流动",
        "size": "1920x1080"   # 横屏
    },
    {
        "model": "veo_3_1-fast",
        "prompt": "城市夜景延时摄影，霓虹灯光流动",
        "size": "1080x1920"   # 竖屏
    }
]

batch_result = client.generate_batch(tasks)
task_ids = [r["task_id"] for r in batch_result["results"] if r.get("success")]
# 对话中不要轮询：直接返回 task_ids，并提示稍后查询
```

---

## 七、查询任务示例

### 查询单个任务
```python
task = client.query_task("task_xxxxxxxxxxxxx")
# {"success": True, "id": "task_xxx", "status": "completed", "url": "https://..."}
```

### 批量查询任务
```python
tasks = client.query_tasks(["task_001", "task_002", "task_003"])
for t in tasks["results"]:
    print(f"{t['task_id']}: {t['status']} - {t.get('url', t.get('error', ''))}")
```

### 查询本地任务列表
```python
# 查询所有任务（最近 50 条）
all_tasks = client.list_tasks()

# 按状态过滤
completed = client.list_tasks(status="completed")
processing = client.list_tasks(status="processing")
```

### 任务统计示例（按天/按类型/成功数量）

```python
from datetime import date
from local_client import get_client

client = get_client()

# 统计今天的任务（按 Veo / Sora / 图片 分类）
today = date.today()
summary = client.summarize_tasks(target_date=today, status=None)

# summary 结构示例：
# {
#   "total": 12,
#   "by_type": {
#     "veo":   {"total": 5, "success": 4, "failed": 1, "ids": ["task_xxx", ...]},
#     "sora":  {"total": 3, "success": 3, "failed": 0, "ids": [...]},
#     "image": {"total": 4, "success": 2, "failed": 2, "ids": [...]}
#   }
# }
```

> **对话说明**：当用户说「我想查询一下今天生成了多少条任务，veo 有多少，sora 有多少，图片有多少，成功有多少，把成功的 ID 发我一下，分类发我」时：
>
> 1. 优先调用 `client.summarize_tasks(target_date=今天, status=None)` 拿到结构化统计。
> 2. 只统计本地任务表中 `video_id` 以 `task_` 开头的记录（严格视为 upstream 任务 ID）。
> 3. 按 Veo / Sora / 图片 三类分别用自然语言说明总数、成功/失败数。
> 4. 把成功的 ID 按类型分别列出，例如：
>    - Veo 成功任务 ID：
>    ```text
>    task_xxxxxxxx
>    task_yyyyyyyy
>    ```
>    - Sora 成功任务 ID：
>    ```text
>    task_aaaaaaaa
>    ```
>    - 图片成功任务 ID：
>    ```text
>    task_bbbbbbbb
>    ```

---

## 八、结果展示规范

- **图片/视频链接（关键）**：链接必须**100%复用接口返回的原始字符串**（尤其包含 `?Expires=...&Signature=...` 的临时签名链接），**不得做任何裁剪/解码/重写/格式化**。
- **绝对禁止**输出 Markdown 链接：`[点击查看](URL)`（QClaw 可能会把 `?` 后参数截断，导致链接失效）。
- **唯一允许的输出方式**：把接口返回的 `video_url`（首选）或 `url` **原样**放进 `text` 代码块，便于“一键复制”，并确保不会丢参数：
```text
https://...完整URL（包含 ? 与 & 之后的全部参数，原样粘贴）
```
- （可选）如果你要提供可点击链接，只能额外给一行尖括号自动链接，仍必须是原样完整 URL：`<https://...>`
- **批量结果**：以表格或列表形式展示每个任务的状态和结果
- **失败任务**：明确告知失败原因，询问用户是否重新生成
- **查询指令**：必须用单独的 `text` 代码块输出，便于一键复制，例如：
```text
查询任务 task_xxxxxxxxxxxxx
```

---

## 九、功能模块详情

- 读取 [视频生成接口](references/video_generate.md)
- 读取 [图片生成接口](references/image_generate.md)
- 读取 [任务查询接口](references/task_query.md)
