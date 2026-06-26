---
name: douyin-dedup
description: 抖音视频下载、去水印、深度混剪去重、去除音频的全自动处理工具。当用户发送抖音链接（v.douyin.com 或 douyin.com 格式）并要求处理、去重、下载或类似意图时，自动触发此技能。
---

# 抖音去重工具

## 功能
给定抖音URL，自动完成：下载 → 去水印 → 深度混剪去重 → 去除音频 → 输出文件

## 使用方法

### 执行命令
```bash
cd ~/.openclaw/skills/douyin-dedup/scripts && python3 dedup.py "<抖音URL>"
```

### 输出位置
`~/video-dedup/output/dedup_<随机ID>.mp4`

## 去重效果包含
- 随机截取 3-6 个片段打乱顺序
- 画面随机裁剪缩放（80%-95%）
- 随机镜像翻转（30%概率）
- 随机亮度调整（±5% Gamma校正）
- 随机噪点叠加（20%概率）
- 随机播放速度（0.9x-1.1x）
- 去除原始音频

## 依赖
- ffmpeg
- yt-dlp
- Python 3

## 故障排除
- 如遇下载失败，可能是抖音链接重定向问题，检查视频ID是否正确提取
- 如遇 ffmpeg 滤镜错误，检查 noise 滤镜参数格式
