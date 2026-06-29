# Agnes Video Generator Skill

生成高质量 AI 视频，基于 Agnes-Video-V2.0 模型。支持文生视频、图生视频、多图视频和关键帧动画。

## 配置

设置环境变量：

```bash
export AGNES_API_KEY="your-api-key"
```

## 使用方法

### 基本文生视频

```bash
node generate.js --prompt "A cinematic shot of a cat walking on the beach at sunset" --num_frames 121 --frame_rate 24 --size 1152x768
```

### 图生视频

```bash
node generate.js --prompt "The woman slowly turns around and looks back at the camera" --image "https://example.com/image.png" --num_frames 121
```

### 多图视频 / 关键帧（需编辑脚本或扩展）

当前脚本支持单图。如需多图或关键帧，可修改脚本在 `body` 中添加 `extra_body.image` 数组和 `extra_body.mode`。

## 参数

| 参数 | 说明 |
|------|------|
| `prompt` | 视频描述（必填） |
| `image` | 图片 URL（图生视频时使用） |
| `num_frames` | 帧数，需满足 `8n+1`（推荐 81/121/241/441） |
| `frame_rate` | 帧率 1–60（默认 24） |
| `size` | 分辨率，如 `1152x768` |
| `seed` | 随机种子，保证可复现 |
| `negative_prompt` | 负向提示词 |
| `extra_mode` | 额外模式，如 `keyframes`（需配合 multi-image） |

## 输出

脚本会轮询直到完成，输出 JSON：

```json
{
  "success": true,
  "url": "https://storage.googleapis.com/agnes-aigc/...mp4",
  "size": "1280x768",
  "seconds": "5.0",
  "video_id": "video_xxx",
  "status": "completed"
}
```

## 注意事项

- 视频生成是异步的，脚本会自动轮询（默认 120 次，每次 5 秒，最长约 10 分钟）
- `num_frames` 必须 ≤ 441
- 默认分辨率 1152×768 (16:9)，可根据需要调整
- 如果任务失败，会在 error 字段中说明

## 示例输出链接格式

```
https://platform-outputs.agnes-ai.space/videos/...
```

或根据文档，实际字段名可能是 `remixed_from_video_id`。
