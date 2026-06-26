---
name: anime-drama
version: "1.0.0"
description: "将小说原文自动转换为动漫短剧。用户输入故事文本，系统自动完成：分镜脚本生成 → 文生图（RH AI应用）→ 图生视频（RH AI应用）→ ffmpeg合并成片。支持竖屏9:16短视频输出。"
homepage: https://github.com/win4r/ClawTeam-OpenClaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3", "curl", "ffmpeg"], "skills": ["runninghub"] },
        "primaryEnv": "RUNNINGHUB_API_KEY"
      }
  }
---

# 动漫短剧生成技能 (Anime Drama Pipeline)

输入小说原文 → 输出竖屏动漫短视频（分镜脚本 + 图片 + 视频片段 + 合并成片）

## 核心流程

```
小说原文
  ↓
分镜脚本生成（按段落拆分为多个镜头）
  ↓
并行/逐个执行：
  ├─ 文生图（RH AI应用 AppId: YOUR_IMAGE_APP_ID，节点 12:value）
  └─ 图生视频（RH AI应用 AppId: YOUR_VIDEO_APP_ID，节点 325:value + 269:image）
  ↓
ffmpeg 合并所有视频片段
  ↓
最终成片（竖屏 1080×1920，MP4）
```

## 必读参考文档

- `{baseDir}/references/pipeline-usage.md` — 完整使用说明
- `{baseDir}/references/ffmpeg-install.md` — ffmpeg 安装指南
- `{baseDir}/references/runninghub-ai-app-notes.md` — RH AI应用调用要点

## 核心脚本

```bash
python3 {baseDir}/scripts/anime_drama_pipeline.py <小说原文文件> [输出目录]
```

## Pipeline 脚本位置

`{baseDir}/scripts/anime_drama_pipeline.py`

## RH API 关键参数（永久记忆）

| 用途 | AppID / 端点 | 节点 |
|------|-------------|------|
| 文生图 | `YOUR_IMAGE_APP_ID` | `12:value`（单节点，直接传 prompt） |
| 图生视频 | `YOUR_VIDEO_APP_ID` | `325:value`（文本）+ `269:image`（图片） |

**图生视频调用前必须先上传图片：**
1. POST `/task/openapi/upload` 上传本地图片
2. 取返回值中的 `fileName`（格式 `api/xxx.png`）
3. 将 `fileName` 作为 `269:image` 的值传入

## 视频合并（ffmpeg）

```bash
# 生成文件列表
cat > /tmp/video_list.txt << 'EOF'
file '/path/shot_001_vid.mp4'
file '/path/shot_002_vid.mp4'
EOF

# 合并（竖屏 1080×1920）
ffmpeg -y -f concat -safe 0 -i /tmp/video_list.txt \
  -c:v libx264 -pix_fmt yuv420p \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  output.mp4
```

ffmpeg 路径（已安装到）：
`/usr/local/lib/python3.10/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`

## 分镜逻辑

默认按 `\n` 换行分割，每段 = 一个镜头，每个镜头生成一张图 + 一段视频。
如需更智能的分镜，可传入 LLM 优化每个镜头的描述文字。

## 输出格式

- 图片：PNG，~1.7-2.0MB/张
- 视频：MP4（H.264 + AAC），每个镜头默认 5 秒
- 最终成片：MP4，1080×1920（竖屏），16:9 源视频自动 pad 为竖屏

## 常见错误处理

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| 文生图失败 | AI 应用未在网页端运行过 | 先在 RH 网页端手动运行一次应用 |
| 图生视频失败 | 图片未上传到 RH | 必须先调用 `/task/openapi/upload` 获取 fileName |
| ffmpeg: command not found | 未安装 ffmpeg | 使用 imageio-ffmpeg 的内置 ffmpeg |
| 超时中断 | 视频生成需 2-5 分钟/镜头 | 脚本可中断后继续运行（已生成的不会重复生成） |

## 中断后继续

脚本支持断点续传：已生成的图片/视频不会重复生成，中断后重新运行即可继续。
