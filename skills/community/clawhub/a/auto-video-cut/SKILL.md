# auto-video-cut

抖音/视频自动剪辑Skill - 自动识别视频中的废话、沉默片段，生成粗剪版本。

## 适用场景

- ✅ 单人出镜视频（vlog、教程、播客、知识分享）
- ❌ 多人对话、采访
- ❌ 音乐/B-roll较多的内容

## 功能

- **场景A - 单视频**：自动从单个视频中选取最佳片段
- **场景B - 批量处理**：处理多个视频，跨视频去重，拼接成片
- **智能评分**：4维度评分（清晰开始/结束、流畅度、自然节奏）
- **内容去重**：基于语音文本的相似度检测
- **自动报告**：生成详细的处理报告

## 前置要求

- Python 3.8+
- FFmpeg（包含ffprobe）
- openai-whipser

### 安装依赖

```bash
# macOS
brew install ffmpeg
pip install openai-whisper

# Ubuntu / Debian
sudo apt install ffmpeg
pip install openai-whisper

# Windows
# 下载 FFmpeg: https://ffmpeg.org/download.html
# 添加到 PATH
pip install openai-whisper
```

## 使用方法

### 场景A：单视频剪辑

```bash
python3 video_editor_auto.py /path/to/video.mp4 ./output
```

### 场景B：批量处理+去重+拼接

```bash
python3 video_editor_auto.py /path/to/videos_folder ./output
```

## 输出

- `*.mp4` - 剪辑后的视频
- `*_报告.md` - 处理报告

## 参数配置

在脚本顶部的 `CONFIG` 字典中修改：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| silence_noise | 静音检测阈值(dB)，越低越严格 | -30 |
| silence_duration | 最小静音时长(秒) | 0.8 |
| min_score | 最低评分(0-100) | 90 |
| min_duration | 最短片段时长(秒) | 15 |
| crf | 视频质量(18=无损) | 18 |

## 调优建议

- 环境嘈杂 → silence_noise 设为 -35
- 片段太碎 → silence_duration 设为 1.0
- 想保留更多候选 → min_score 设为 85

## 工作流程

```
拍摄素材 → 归档到文件夹 → 运行脚本 → AI分析+剪辑 → 输 出粗剪 → 剪映精修 → 完成
```

## 来源

基于 gilbertwuu/Auto-Cut-video-A-Roll 项目改编
