---
name: alibaba-ai-video-wan-video
description: Alibaba Cloud Wanx Video Generation - Text to Video, Image to Video, Video Editing
homepage: https://help.aliyun.com/zh/model-studio/video-generation
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "env": ["DASHSCOPE_API_KEY"] },
        "install": [],
      },
  }
---

# 阿里云万相视频生成 (Wanx Video)

专业的视频生成和处理服务，支持文生视频、图生视频、视频编辑等功能。

## 支持的模型

### 文生视频 (Text-to-Video)

| 模型 | 类型 | 时长 | 分辨率 | 说明 |
|------|------|------|--------|------|
| **wan2.6-t2v** | 有声视频 | 5-15s | 720P/1080P | ⭐最新推荐 |
| wan2.5-t2v-preview | 有声视频 | 5-10s | 480P/720P/1080P | 推荐 |
| wan2.2-t2v-plus | 无声视频 | 5s | 480P/1080P | 稳定性高 |
| wan2.1-t2v-turbo | 无声视频 | 5s | 480P/720P | 快速 |
| wan2.1-t2v-plus | 无声视频 | 5s | 720P | 高质量 |

### 图生视频 (Image-to-Video)

| 模型 | 说明 |
|------|------|
| wanx-i2v-first-frame | 基于首帧生成视频 |
| wanx-i2v-first-last-frame | 基于首尾帧生成视频 |

### 人像动画

| 模型 | 说明 |
|------|------|
| wanx-digital-human | 数字人对口型 ⭐推荐 |
| wanx-animate-anyone | 舞动人像 |
| wanx-emo | 悦动人像 |
| wanx-live-portrait | 灵动人像 |

### 视频编辑

| 模型 | 说明 |
|------|------|
| wanx-video-edit | 通用视频编辑 |
| wanx-video-extend | 视频延展 |
| wanx-video-style | 风格重绘 |

## 快速开始

### 文生视频
```bash
{baseDir}/scripts/wanx-video.sh \
  "一只小猫在草地上玩耍" \
  --out /tmp/cat.mp4 \
  --model wan2.6-t2v \
  --duration 5
```

### 图生视频
```bash
{baseDir}/scripts/wanx-i2v.sh \
  /tmp/input.jpg \
  --out /tmp/output.mp4 \
  --prompt "让画面动起来"
```

### 数字人
```bash
{baseDir}/scripts/wanx-digital-human.sh \
  --image /tmp/portrait.jpg \
  --audio /tmp/voice.mp3 \
  --out /tmp/talking.mp4
```

## 参数说明

### 文生视频参数
- `--model`: 模型名称（默认：wan2.1-t2v-turbo）
- `--duration`: 视频时长（秒，默认：5）
- `--resolution`: 分辨率（480p/720p/1080p）
- `--out`: 输出文件路径（必填）
- `--negative-prompt`: 负向提示词（可选）

### 图生视频参数
- `--image`: 输入图片路径
- `--prompt`: 提示词
- `--out`: 输出文件路径

## 示例

### 示例 1：简单场景
```bash
{baseDir}/scripts/wanx-video.sh \
  "日落时分的海滩，海浪轻拍岸边，电影感" \
  --out /tmp/beach.mp4 \
  --model wan2.6-t2v \
  --duration 10 \
  --resolution 1080p
```

### 示例 2：古诗意境
```bash
{baseDir}/scripts/wanx-video.sh \
  "床前明月光，疑是地上霜。举头望明月，低头思故乡。古典中国风，水墨画" \
  --out /tmp/jingyesi.mp4
```

### 示例 3：产品宣传
```bash
{baseDir}/scripts/wanx-video.sh \
  "现代科技产品，简洁设计，白色背景，缓慢旋转展示" \
  --out /tmp/product.mp4 \
  --model wan2.2-t2v-plus
```

## 注意事项

1. **API Key**: 需要配置阿里云百炼 API Key
2. **服务开通**: 需要在百炼控制台开通视频生成服务
3. **异步生成**: 视频生成是异步的，需要等待 1-5 分钟
4. **费用**: 视频生成会产生费用
5. **内容限制**: 不能生成违规内容

## 故障排除

**问题：Model not exist**
- 检查模型名称是否正确
- 确认 API Key 已开通视频生成服务
- 访问 https://bailian.console.aliyun.com/ 开通服务

**问题：超时**
- 视频生成需要时间，耐心等待
- 检查网络连接

**问题：生成质量不佳**
- 优化提示词，增加细节描述
- 尝试不同的模型
- 添加负向提示词排除不想要的元素

## 相关链接

- [视频生成文档](https://help.aliyun.com/zh/model-studio/video-generation)
- [API 参考](https://help.aliyun.com/zh/model-studio/text-to-video-api-reference)
- [在线体验](https://bailian.console.aliyun.com/cn-beijing?tab=model#/efm/model_experience_center/vision)
- [Prompt 指南](https://help.aliyun.com/zh/model-studio/text-to-video-prompt)
