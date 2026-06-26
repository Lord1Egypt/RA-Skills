# 视频转录工作流

## 支持的视频源

- YouTube
- Bilibili
- 直接视频链接（MP4, WebM）
- 其他 yt-dlp 支持的网站

## 工作流程

```
视频 URL/文件
    ↓
[1] 下载视频 (yt-dlp/ffmpeg)
    ↓
[2] 提取音频 (ffmpeg → WAV 16kHz)
    ↓
[3] FunASR 转录
    ↓
[4] 输出文字
```

## 命令示例

### 转录本地视频

```bash
python3 scripts/video-transcribe.py --audio /path/to/video.mp4
```

### 从网页提取视频

```bash
python3 scripts/video-transcribe.py https://www.youtube.com/watch?v=xxx --extract
```

### 从视频 URL 直接转录

```bash
python3 scripts/video-transcribe.py https://example.com/video.mp4
```

### 保留临时文件（调试）

```bash
python3 scripts/video-transcribe.py <url> --keep
```

## Python API

```python
from video_transcribe import VideoTranscriber

transcriber = VideoTranscriber()

# 处理视频 URL
text = transcriber.process_video("https://example.com/video.mp4")

# 从网页提取
text = transcriber.process_video("https://youtube.com/watch?v=xxx", extract_video=True)

# 直接转录音频
text = transcriber.transcribe_audio("/path/to/audio.wav")
```

## 临时文件

默认自动清理临时文件。使用 `--keep` 保留：

```bash
python3 scripts/video-transcribe.py <url> --keep
# 临时文件保存在 /tmp/video_transcribe_xxx/
```

## 常见问题

### YouTube 下载失败

更新 yt-dlp：

```bash
pip install -U yt-dlp
```

### 音频提取失败

确保 ffmpeg 已安装：

```bash
ffmpeg -version
```

### 格式不支持

先转换格式：

```bash
ffmpeg -i input.mkv -c:v libx264 -c:a aac output.mp4
```
