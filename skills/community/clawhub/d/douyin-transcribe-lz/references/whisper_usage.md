# Whisper 使用参考

## 模型选择

| 模型 | 参数量 | 磁盘大小 | 速度 | 中文准确率 |
|------|--------|----------|------|-----------|
| tiny  | ~39M   | ~75MB    | 10x  | 一般      |
| base  | ~74M   | ~140MB   | 7x   | 可用      |
| small | ~244M  | ~480MB   | 4x   | 较好      |
| medium | ~769M | ~1.4GB  | 2x   | **推荐**  |
| large | ~1550M | ~2.9GB  | 1x   | 最高      |

**推荐：medium** — 中文准确率与 large 差距不大，速度合理，首次下载后缓存。

## 常用参数

```python
result = model.transcribe(
    audio_path,
    language="zh",       # 强制中文，减少语种混淆
    task="transcribe",    # "transcribe" 或 "translate"（译为英文）
    verbose=True,         # 显示进度
    temperature=0.0,      # 采样温度，越低越确定性（推荐 0.0）
    best_of=5,            # 候选数，越高越慢越准
    beam_size=5,          # beam 搜索宽，越高越慢越准
    initial_prompt="以下是一段中文对话：",  # 可提升开头准确率
)
```

## 输出结构

```python
{
    "text": "完整连续文本（无标点）",
    "segments": [
        {
            "id": 0,
            "start": 0.0,      # 秒
            "end": 3.4,        # 秒
            "text": "文字内容",
            "tokens": [12345, 67890],
        },
        ...
    ],
    "language": "zh"
}
```

## 模型缓存管理

Whisper 模型首次下载后缓存于 `~/.cache/whisper/`（Windows: `%USERPROFILE%\.cache\whisper\`）。

### 缓存损坏检测与修复

模型下载中断或磁盘错误可能导致缓存损坏，表现为运行时报 `SIGABRT` 崩溃。

**自动修复**（`fetch_douyin_video.py` 已内置）：
- 脚本内 `load_whisper_safe()` 会检测模型文件是否小于 500MB（正常 medium 为 ~1.4GB）
- 若损坏则自动删除并重新下载

**手动修复**：
```bash
# 删除疑似损坏的模型缓存
rm ~/.cache/whisper/medium.pt
# 下次运行 Whisper 时自动重新下载
```

### 手动下载（网络慢时）

```bash
# medium 模型 (1.42 GB)
wget https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt \
     -O ~/.cache/whisper/medium.pt
```

---

## 常见问题

**Q: ffmpeg 未找到**
```python
import imageio_ffmpeg
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
# 或获取路径并注入 PATH
```

**Q: 音频提取失败（MP4 无声音流）**
- 使用 ffmpeg 重新封装：`ffmpeg -i input.mp4 -vn -acodec copy output.aac`
- 或转换为 WAV：`ffmpeg -i input.mp4 -vn -ar 16000 -ac 1 output.wav`，再用 `whisper.load_audio()` + `whisper.pad_or_trim()`

**Q: 中文夹杂英文专有名词识别差**
- 设置 `initial_prompt` 提供上下文风格提示
- 例如：`initial_prompt="这是一个关于 AI 和编程的技术视频，常见词包括：Python、API、Agent"`

**Q: 如何提取纯音频？**
```python
audio = whisper.load_audio(video_path)  # 自动用 ffmpeg 提取
audio = whisper.pad_or_trim(audio)
# 直接传 audio 数组给 model.decode()
```
