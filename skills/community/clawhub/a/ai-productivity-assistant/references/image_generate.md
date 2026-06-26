# 图片生成接口

通过本地客户端接口提交图片生成任务（文生图 / 图生图）。

## 本地接口

`POST http://127.0.0.1:17321/api/generate`

## 支持的图片模型

| model 参数 | 说明 | 分辨率 |
|-----------|------|--------|
| `nano_banana_2` | 标准版，速度最快 | 标准 |
| `nano_banana_pro` | Pro 版，标准分辨率 | 标准 |
| `nano_banana_pro-1K` | Pro 版，1K 分辨率 | 1K |
| `nano_banana_pro-2K` | Pro 版，2K 分辨率 | 2K |
| `nano_banana_pro-4K` | Pro 版，4K 分辨率 | 4K |

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
|-----|------|------|------|
| model | string | 是 | 见上方模型列表 |
| prompt | string | 是 | 提示词，最大 10000 字符 |
| metadata | object | 否 | 图片生成额外参数 |
| metadata.aspectRatio | string | 否 | 宽高比：`1:1` / `9:16` / `16:9` / `auto`，默认 `auto` |
| metadata.urls | string[] | 否 | 参考图片 URL 或 Base64 列表（最多 5 张）。**传此参数 = 图生图模式，不传 = 文生图模式** |

## 响应参数

| 参数 | 类型 | 说明 |
|-----|------|------|
| success | bool | 是否提交成功 |
| task_id | string | 任务 ID |
| status | string | 初始状态，通常为 `queued` |
| model | string | 使用的模型 |

## 示例

### 文生图（16:9 横图，标准）
```python
from local_client import get_client
client = get_client()

result = client.generate({
    "model": "nano_banana_2",
    "prompt": "美丽的日出风景，金色阳光洒在宁静湖面，远处连绵山脉，写实摄影风格",
    "metadata": {
        "aspectRatio": "16:9",
        "urls": []
    }
})

final = client.wait_for_result(result["task_id"])
print(final["url"])  # https://...
# 展示图片：![生成结果](url)
```

### 文生图（9:16 竖图，1K 高清）
```python
result = client.generate({
    "model": "nano_banana_pro-1K",
    "prompt": "时尚女性人像，工作室灯光，专业摄影，高清质感",
    "metadata": {
        "aspectRatio": "9:16",
        "urls": []
    }
})
final = client.wait_for_result(result["task_id"])
```

### 文生图（1:1 正方形）
```python
result = client.generate({
    "model": "nano_banana_2",
    "prompt": "产品主图：一款白色无线耳机，白色背景，简洁干净",
    "metadata": {
        "aspectRatio": "1:1",
        "urls": []
    }
})
final = client.wait_for_result(result["task_id"])
```

### 图生图（URL 参考图）
```python
result = client.generate({
    "model": "nano_banana_2",
    "prompt": "将这张图片转换成梵高油画风格，保留主体构图和色调",
    "metadata": {
        "aspectRatio": "auto",
        "urls": ["https://example.com/reference.jpg"]
    }
})
final = client.wait_for_result(result["task_id"])
```

### 图生图（多张参考图）
```python
result = client.generate({
    "model": "nano_banana_pro",
    "prompt": "融合这两张图片的风格，生成一张新的风景图",
    "metadata": {
        "aspectRatio": "16:9",
        "urls": [
            "https://example.com/style_ref.jpg",
            "https://example.com/content_ref.jpg"
        ]
    }
})
final = client.wait_for_result(result["task_id"])
```

## 批量示例

### 批量文生图（产品多角度）
```python
tasks = [
    {
        "model": "nano_banana_pro-1K",
        "prompt": "产品主图：智能手表，白色背景，专业摄影",
        "metadata": {"aspectRatio": "1:1", "urls": []}
    },
    {
        "model": "nano_banana_pro-1K",
        "prompt": "产品场景图：智能手表佩戴在手腕上，户外运动",
        "metadata": {"aspectRatio": "16:9", "urls": []}
    },
    {
        "model": "nano_banana_pro-1K",
        "prompt": "产品竖图：智能手表展示，时尚简约风格",
        "metadata": {"aspectRatio": "9:16", "urls": []}
    },
]

batch = client.generate_batch(tasks)
task_ids = [r["task_id"] for r in batch["results"] if r.get("success")]
finals = client.wait_for_results(task_ids, timeout=300)

for i, f in enumerate(finals):
    if f["status"] == "completed":
        print(f"图片{i+1}: ![image]({f['url']})")
```

### 批量图生图（风格迁移）
```python
source_images = [
    "https://example.com/photo1.jpg",
    "https://example.com/photo2.jpg",
    "https://example.com/photo3.jpg",
]

tasks = [
    {
        "model": "nano_banana_2",
        "prompt": "转换成水彩画风格，色彩明亮，笔触柔和",
        "metadata": {"aspectRatio": "auto", "urls": [url]}
    }
    for url in source_images
]

batch = client.generate_batch(tasks)
task_ids = [r["task_id"] for r in batch["results"] if r.get("success")]
finals = client.wait_for_results(task_ids, timeout=300)
```

## 注意事项

1. **模式判断**：`metadata.urls` 为空列表或不传 = 文生图；包含图片 = 图生图
2. **参考图数量**：最多 5 张参考图片
3. **参考图格式**：支持 URL（推荐）或 Base64 Data URL（`data:image/jpeg;base64,...`）
4. **宽高比**：通过 `metadata.aspectRatio` 控制，`auto` 由模型自动决定
5. **任务模式**：异步任务，需轮询 `/api/task/{task_id}` 查询结果
6. **结果展示**：完成后 `url` 字段为图片地址，可直接用 `![image](url)` 渲染
