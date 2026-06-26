# 视频生成接口

通过本地客户端接口提交视频生成任务，客户端代理转发到 AI 服务。

## 本地接口

`POST http://127.0.0.1:17321/api/generate`

## 支持的视频模型

### Sora 模型

| model 参数 | 说明 |
|-----------|------|
| `sora-2-landscape-10s` | Sora 2 横屏 10 秒 |
| `sora-2-portrait-10s` | Sora 2 竖屏 10 秒 |
| `sora-2-landscape-15s` | Sora 2 横屏 15 秒 |
| `sora-2-portrait-15s` | Sora 2 竖屏 15 秒 |
| `sora-2-pro-landscape-25s` | Sora 2 Pro 横屏 25 秒 |
| `sora-2-pro-portrait-25s` | Sora 2 Pro 竖屏 25 秒 |
| `sora-2-pro-landscape-hd-15s` | Sora 2 Pro 横屏 HD 15 秒 |
| `sora-2-pro-portrait-hd-15s` | Sora 2 Pro 竖屏 HD 15 秒 |

### Veo 模型

| model 参数 | 说明 |
|-----------|------|
| `veo_3_1-fast` | Veo 通用模型（文生视频 / 参考图模式） |
| `veo_3_1-fast-fl` | Veo 首尾帧模式（1-2 张图作首尾帧） |

## 请求参数

### Sora 文生视频

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| model | string | 是 | 见上方模型列表 |
| prompt | string | 是 | 提示词 |
| style | string | 否 | 视频风格 |

### Sora 图生视频（URL）

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| model | string | 是 | 见上方模型列表 |
| prompt | string | 是 | 提示词 |
| image_url | string | 是 | 参考图片的可访问 URL |
| style | string | 否 | 视频风格 |

### Veo 文生视频

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| model | string | 是 | `veo_3_1-fast` |
| prompt | string | 是 | 提示词 |
| size | string | 是 | 视频尺寸：`1920x1080`（横屏）/ `1080x1920`（竖屏）/ `1280x720` / `720x1280` |

### Veo 首尾帧模式

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| model | string | 是 | `veo_3_1-fast-fl` |
| prompt | string | 是 | 提示词 |
| size | string | 是 | 视频尺寸 |
| image_url | string | 是 | 首帧图片 URL（如需尾帧，使用 input_reference 参数） |

## 响应参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| success | bool | 是否提交成功 |
| task_id | string | 任务 ID，用于轮询查询 |
| status | string | 初始状态，通常为 `queued` |
| model | string | 使用的模型 |
| prompt | string | 提交的提示词 |
| submitted_at | string | 提交时间 |

## 示例

### Sora 文生视频
```python
from local_client import get_client
client = get_client()

result = client.generate({
    "model": "sora-2-landscape-10s",
    "prompt": "一只可爱的橘猫在阳光明媚的花园里玩耍，镜头缓慢推进"
})
print(result["task_id"])  # task_xxxxxxxxxxxxx
```

### Sora 图生视频
```python
result = client.generate({
    "model": "sora-2-portrait-10s",
    "prompt": "让画面动起来，人物微微转头微笑",
    "image_url": "https://example.com/photo.jpg"
})
```

### Veo 横屏文生视频
```python
result = client.generate({
    "model": "veo_3_1-fast",
    "prompt": "夕阳下的海边，海浪轻轻拍打礁石",
    "size": "1920x1080"
})
```

### Veo 竖屏文生视频
```python
result = client.generate({
    "model": "veo_3_1-fast",
    "prompt": "城市街头人流涌动，快节奏都市生活",
    "size": "1080x1920"
})
```

## 批量示例

```python
tasks = [
    {"model": "sora-2-landscape-10s", "prompt": "春天樱花飘落"},
    {"model": "sora-2-landscape-10s", "prompt": "夏日海浪拍岸"},
    {"model": "sora-2-landscape-10s", "prompt": "秋天枫叶飘落"},
    {"model": "sora-2-landscape-10s", "prompt": "冬日雪花纷飞"},
]

batch = client.generate_batch(tasks)
task_ids = [r["task_id"] for r in batch["results"] if r.get("success")]
finals = client.wait_for_results(task_ids, timeout=600)

for i, f in enumerate(finals):
    if f["status"] == "completed":
        print(f"第{i+1}个: {f['url']}")
```

## 注意事项

1. **异步任务**：提交后返回 task_id，需轮询 `/api/task/{task_id}` 查询结果
2. **Veo 必须填 size**：Veo 模型的 size 参数为必填，Sora 不需要
3. **图生视频使用 URL**：通过 `image_url` 传入可公开访问的图片 URL
4. **横竖屏选择**：Sora 通过模型名称区分（landscape/portrait），Veo 通过 size 参数区分
