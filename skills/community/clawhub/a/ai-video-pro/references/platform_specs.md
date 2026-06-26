# 平台发布规格说明

## 微博 (Weibo)

| 参数 | 规格 |
|------|------|
| 最大分辨率 | 1920x1080 (1080p) |
| 最大文件大小 | 500MB |
| 最大时长 | 15分钟 |
| 推荐比例 | 16:9 (横屏), 9:16 (竖屏) |
| 视频格式 | MP4 |
| 视频编码 | H.264 |
| 音频编码 | AAC |
| 帧率 | 24-60fps |
| 码率建议 | 2-8 Mbps |

**API:** 微博开放平台 `https://api.weibo.com/2/`
- 上传: `statuses/upload_video`
- 认证: OAuth 2.0 Access Token
- 环境变量: `WEIBO_ACCESS_TOKEN`

**FFmpeg 转码命令:**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -movflags +faststart \
  -vf "scale='min(1920,iw)':'min(1080,ih)'" output_weibo.mp4
```

## 小红书 (Xiaohongshu / RED)

| 参数 | 规格 |
|------|------|
| 最大分辨率 | 1080x1440 (3:4) 或 1080x1080 (1:1) |
| 最大文件大小 | 100MB |
| 最大时长 | 15分钟 |
| 推荐比例 | 3:4 (推荐), 1:1, 9:16 |
| 视频格式 | MP4 |
| 视频编码 | H.264 |
| 音频编码 | AAC |
| 帧率 | 30fps |
| 封面 | 必须，1080x1440 推荐 |

**注意:** 小红书无官方开放 API，发布需通过 Cookie 模拟或手动上传。
- 使用 Cookie 模拟存在 TOS 违规风险
- 环境变量: `XHS_COOKIE` (可选)
- 建议方案: 导出发布就绪的文件 + 封面图，由用户手动上传

**FFmpeg 转码命令 (3:4 比例):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -movflags +faststart \
  -vf "scale=1080:1440:force_original_aspect_ratio=decrease,pad=1080:1440:-1:-1:black" \
  output_xhs.mp4
```

## 抖音 (Douyin / TikTok)

| 参数 | 规格 |
|------|------|
| 最大分辨率 | 1080x1920 (9:16) |
| 最大文件大小 | 128MB |
| 最大时长 | 15分钟 (普通), 60分钟 (部分账号) |
| 推荐比例 | 9:16 (强烈推荐竖屏) |
| 视频格式 | MP4 |
| 视频编码 | H.264 |
| 音频编码 | AAC |
| 帧率 | 30fps |
| 码率建议 | 3-6 Mbps |

**API:** 抖音开放平台 `https://open.douyin.com/`
- 上传: `/api/douyin/v1/video/upload/`
- 发布: `/api/douyin/v1/video/create/`
- 认证: OAuth 2.0 Access Token
- 环境变量: `DOUYIN_ACCESS_TOKEN`

**FFmpeg 转码命令 (9:16 竖屏):**
```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -movflags +faststart \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1:black" \
  output_douyin.mp4
```

## 云存储

### 阿里云 OSS
- 环境变量: `ALIYUN_ACCESS_KEY_ID`, `ALIYUN_ACCESS_KEY_SECRET`, `ALIYUN_OSS_BUCKET`
- SDK: `oss2`

### 腾讯云 COS
- 环境变量: `TENCENT_SECRET_ID`, `TENCENT_SECRET_KEY`, `TENCENT_COS_BUCKET`
- SDK: `cos-python-sdk-v5`

### AWS S3
- 环境变量: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`
- SDK: `boto3`

## 通用转码最佳实践

1. **始终使用 H.264 编码** — 兼容性最广
2. **音频使用 AAC** — 所有平台都支持
3. **添加 `movflags +faststart`** — 优化网络流播放
4. **CRF 值 18-23** — 质量和文件大小的平衡
5. **保留原始文件** — 转码输出到新文件，不覆盖原始
