# 飞书 AI 视频剪辑 Skill - MVP

⚡ **OpenClaw Skill 大师培训体系 - 实战项目**

---

## 📋 概述

本 Skill 实现基于飞书的 AI 视频剪辑功能，支持语音识别、智能裁剪、字幕生成等核心功能。

### MVP 功能范围

| 功能 | 状态 | 说明 |
|------|------|------|
| **视频下载** | ✅ | 从飞书云空间下载视频 |
| **语音转文字** | ✅ | 使用 Whisper 进行 ASR |
| **静音检测** | ✅ | 自动识别并删除静音片段 |
| **视频裁剪** | ✅ | 基于时间戳裁剪视频 |
| **字幕生成** | ✅ | 自动生成 SRT 字幕 |
| **结果上传** | ✅ | 剪辑完成自动上传到飞书 |

---

## 🏗️ 架构设计

### 核心流程

```
用户上传视频到飞书
    ↓
发送指令：@视频助手 剪辑这个视频
    ↓
Skill 下载视频到本地
    ↓
AI 分析（语音识别 + 静音检测）
    ↓
生成剪辑方案
    ↓
FFmpeg 执行剪辑
    ↓
上传结果到飞书云空间
    ↓
返回剪辑后的视频链接
```

### 技术栈

| 组件 | 技术选型 |
|------|----------|
| 视频处理 | FFmpeg |
| 音频分析 | librosa, pydub |
| 语音识别 | Whisper (openai-whisper) |
| 字幕生成 | pysrt |
| 飞书集成 | 飞书开放 API |

---

## 🚀 安装与配置

### 步骤 1：安装系统依赖

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# macOS
brew install ffmpeg

# CentOS/RHEL
sudo yum install -y ffmpeg
```

### 步骤 2：安装 Skill

```bash
claw skill install feishu-video-editor
```

### 步骤 3：安装 Python 依赖

```bash
cd ~/openclaw-skills/feishu-video-editor
pip install -r requirements.txt
```

### 步骤 4：配置

编辑 `config.json`：

```json
{
  "whisper_model": "base",
  "output_dir": "~/Videos/edited",
  "auto_upload": true,
  "silent_threshold": -50,
  "min_silent_duration": 1.0
}
```

---

## 💡 使用示例

### 示例 1：删除静音片段

```
你：@视频助手 把这个视频中的静音部分剪掉
视频助手：🎬 开始处理视频...
视频助手：📊 检测到 5 段静音，总时长 12 秒
视频助手：✂️ 剪辑完成！
视频助手：✅ 已上传到云空间：[剪辑后的视频.mp4](链接)
```

### 示例 2：按时间裁剪

```
你：@视频助手 裁剪视频 00:01:30 到 00:02:45
视频助手：✂️ 裁剪中...
视频助手：✅ 完成！时长：1 分 15 秒
```

### 示例 3：生成字幕

```
你：@视频助手 给这个视频生成字幕
视频助手：🎤 语音识别中...
视频助手：📝 生成字幕文件...
视频助手：✅ 字幕已生成：[字幕.srt](链接)
```

### 示例 4：提取音频

```
你：@视频助手 提取这个视频的音频
视频助手：🎵 提取中...
视频助手：✅ 音频已提取：[音频.mp3](链接)
```

---

## 🔧 可用命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `/video_editor trim_silence` | 删除静音片段 | 上传视频后发送 |
| `/video_editor crop` | 按时间裁剪 | `crop 00:01:00 00:02:30` |
| `/video_editor subtitle` | 生成字幕 | 上传视频后发送 |
| `/video_editor extract_audio` | 提取音频 | 上传视频后发送 |
| `/video_editor merge` | 合并多个视频 | `merge video1.mp4 video2.mp4` |
| `/video_editor help` | 显示帮助 | - |

---

## ⚙️ 配置说明

### config.json

```json
{
  "whisper_model": "base",
  "output_dir": "~/Videos/edited",
  "auto_upload": true,
  "silent_threshold": -50,
  "min_silent_duration": 1.0,
  "ffmpeg_preset": "medium",
  "max_file_size_mb": 100
}
```

### 配置项说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `whisper_model` | base | Whisper 模型：tiny/base/small/medium/large |
| `output_dir` | ~/Videos/edited | 输出目录 |
| `auto_upload` | true | 自动上传到飞书云空间 |
| `silent_threshold` | -50 | 静音检测阈值（dB） |
| `min_silent_duration` | 1.0 | 最小静音时长（秒） |
| `ffmpeg_preset` | medium | FFmpeg 编码预设 |
| `max_file_size_mb` | 100 | 最大文件大小限制 |

---

## 📊 性能参考

| 视频时长 | 处理时间（M1 Mac） | 处理时间（Intel i7） |
|----------|-------------------|---------------------|
| 1 分钟 | ~30 秒 | ~60 秒 |
| 5 分钟 | ~2 分钟 | ~5 分钟 |
| 10 分钟 | ~5 分钟 | ~12 分钟 |

**注意：** Whisper 语音识别是主要耗时步骤。

---

## ⚠️ 注意事项

### 1. 文件大小限制

飞书云空间单文件限制 **100MB**，超过需要：
- 压缩视频质量
- 或分段处理

### 2. 处理时长

视频剪辑是 CPU 密集型任务：
- 建议在服务器端运行
- 或设置超时限制（默认 10 分钟）

### 3. 隐私考虑

视频会下载到本地处理：
- 处理完成后自动清理
- 敏感视频建议本地运行

---

## 🔄 后续优化（TODO）

- [ ] 支持更多视频格式
- [ ] 添加视频压缩功能
- [ ] 智能高光检测
- [ ] 转场效果
- [ ] 批量处理
- [ ] 云端分布式处理
- [ ] 视频预览卡片

---

## 📝 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-03-21 | MVP 版本，核心功能实现 |

---

## 🎓 学习价值

本 Skill 涵盖：

- ✅ FFmpeg 视频处理
- ✅ Whisper 语音识别
- ✅ 音频分析（librosa）
- ✅ 飞书云空间 API
- ✅ 异步任务处理
- ✅ 文件上传下载

---

**作者**: Spark ⚡  
**创建时间**: 2026-03-21  
**GitHub**: https://github.com/rfdiosuao/openclaw-skills/tree/main/feishu-video-editor
