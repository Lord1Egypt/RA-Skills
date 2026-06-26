# AIPing 支持的模型列表

## 图片生成模型

| 模型 | 说明 | 垫图支持 | 宽高比 |
|------|------|----------|--------|
| `Doubao-Seedream-4.0` | 豆包·即梦 4.0 | ✅ | 多种 |
| `Doubao-Seedream-4.5` | 豆包·即梦 4.5 | ✅ | 多种 |
| `Doubao-Seedream-5.0-lite` | 豆包·即梦 5.0 轻量版 | ✅ | 多种 |
| `Kling-V1` | 可灵 1.0 | ❌ | 需指定 aspect_ratio |
| `Kling-V1.5` | 可灵 1.5 | ❌ | 多种 |
| `Kling-V2` | 可灵 2.0 | ❌ | 多种 |
| `Kling-V2.1` | 可灵 2.1 | ❌ | 多种 |
| `Kling-V2-New` | 可灵 2.0 新版 | ❌ | 多种 |
| `Qwen-Image` | 通义千问图像 | ❌ | 多种 |
| `Qwen-Image-2.0` | 千问 2.0 | ❌ | 多种 |
| `Qwen-Image-2.0-Pro` | 千问 2.0 专业版 | ❌ | 多种 |
| `Qwen-Image-Plus` | 千问增强版 | ❌ | 多种 |
| `Qwen-Image-Edit` | 千问图像编辑 | ✅ | 多种 |
| `Qwen-Image-Edit-Plus` | 千问编辑增强版 | ✅ | 多种 |
| `Qwen-Image-Edit-2509-SophNet` | 千问SophNet版 | ✅ | 多种 |
| `GLM-Image` | 智谱图像 | ❌ | 多种 |
| `Gemini-3.1-Flash-Image-Preview` | Gemini 图像 | ❌ | 多种 |
| `Gemini-3-Pro-Image-Preview` | Gemini 专业图像 | ❌ | 多种 |
| `HunyuanImage-3.0` | 腾讯混元 3.0 | ❌ | 多种 |
| `Wan2.5-I2I-Preview` | 阿里 Wan 图生图 | ✅ | 多种 |
| `Wan2.5-T2I-Preview` | 阿里 Wan 文生图 | ❌ | 多种 |
| `Kolors` | Kolors 图像 | ❌ | 多种 |
| `即梦图片生成 4.0` | 即梦 4.0 | ✅ | 多种 |
| `即梦文生图 3.0` | 即梦 3.0 | ✅ | 多种 |
| `即梦文生图 3.1` | 即梦 3.1 | ✅ | 多种 |

## 视频生成模型

| 模型 | mode | aspect_ratio | 说明 |
|------|------|-------------|------|
| `Kling-V2.6` | std | 16:9, 9:16, 1:1 | 稳定版，~60s 生成 |
| `Kling-V3-Omni` | std/pro | 16:9, 9:16, 1:1 | 最新全能版，推荐 pro 模式，~120s |

### 视频参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型名，如 `Kling-V3-Omni` |
| `prompt` | string | 画面描述，建议英文效果更好 |
| `seconds` | string | 时长，默认 "5"（必须是字符串） |
| `mode` | string | `std`（标准）或 `pro`（专业，效果更好但更慢） |
| `aspect_ratio` | string | `16:9`（横屏）、`9:16`（竖屏）、`1:1`（方形） |

### 验证过的参数组合

```bash
# Kling-V2.6 标准模式
model="Kling-V2.6", mode="std", aspect_ratio="16:9", seconds="5"  # ✅ ~61s

# Kling-V3-Omni 专业模式
model="Kling-V3-Omni", mode="pro", aspect_ratio="1:1", seconds="5"  # ✅ ~122s
```

## 垫图（参考图）使用方法

部分模型支持通过 `image` 参数传入参考图 URL：

```json
{
  "model": "Doubao-Seedream-5.0-lite",
  "prompt": "一个宇航员在都市街头漫步",
  "negative_prompt": "模糊，低质量",
  "image": "http://example.com/reference.jpg"
}
```

支持的垫图模型：Doubao-Seedream 系列、Qwen-Image-Edit 系列、Wan2.5-I2I-Preview、即梦系列等。
