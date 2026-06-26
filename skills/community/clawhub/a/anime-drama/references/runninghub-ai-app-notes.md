# RH AI 应用调用要点

## 前提条件

AI 应用必须先在 RH 网页端**手动成功运行过至少一次**，API 才能正常调用。

## 文生图应用 (AppID: YOUR_IMAGE_APP_ID)

单节点工作流，调用最简单：

```bash
python3 runninghub_app.py \
  --run YOUR_IMAGE_APP_ID \
  --node "12:value=你的英文提示词" \
  -o /tmp/output.png \
  --api-key <API_KEY>
```

节点信息：
- `nodeId: 12`
- `fieldName: value`
- `fieldType: STRING`
- `fieldData: ["STRING", {"multiline": true}]

## 图生视频应用 (AppID: YOUR_VIDEO_APP_ID)

双节点工作流，必须先上传图片：

### Step 1: 上传图片

```bash
curl -X POST "https://www.runninghub.cn/task/openapi/upload" \
  -H "Host: www.runninghub.cn" \
  -F "apiKey=<API_KEY>" \
  -F "fileType=input" \
  -F "file=@/path/to/image.png"
```

返回示例：
```json
{
  "code": 0,
  "data": {
    "fileName": "api/xxxx.png"
  }
}
```

### Step 2: 提交图生视频任务

```bash
python3 runninghub_app.py \
  --run YOUR_VIDEO_APP_ID \
  --node "325:value=英文视频提示词" \
  --node "269:image=api/xxxx.png" \
  -o /tmp/output.mp4 \
  --api-key <API_KEY>
```

节点信息：
- `325:value` — 文本提示词（STRING, multiline）
- `269:image` — 图片 fileName（IMAGE 类型，上传后返回的值）

## 提示词优化建议

### 图片提示词（英文）
```
Anime cinematic scene: [场景描述], high quality anime art style, dramatic lighting, vibrant colors, detailed background, anime key visual, 4K
```

### 视频提示词（英文）
```
[场景描述], subtle camera movement, cinematic anime style, smooth motion, dramatic lighting, 4K
```

## 轮询机制

AI 应用任务通过标准轮询获取结果，`runninghub_app.py` 内部已实现：
- 轮询间隔：5秒
- 最大等待：1200秒（20分钟）
- 网络抖动时自动重试（最多3次）
