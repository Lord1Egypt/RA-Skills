## 音频后期处理规范

### 标准处理流程

```
原始音频 → 降噪 → 音量标准化 → [背景音乐混音] → 格式转换 → 输出
```

### 降噪处理

```python
from pydub import AudioSegment
from pydub.effects import normalize

audio = AudioSegment.from_file("input.mp3")

# 简单降噪：去除静音段
audio = audio.strip_silence(silence_thresh=-40)
```

### 音量标准化

目标响度：**-14 LUFS**（符合流媒体平台标准）

```python
# 使用 ffmpeg 标准化
import subprocess
subprocess.run([
    "ffmpeg", "-i", "input.mp3",
    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
    "-ar", "44100",
    "output_normalized.mp3"
])
```

### 背景音乐混音

```python
from pydub import AudioSegment

voice = AudioSegment.from_mp3("voice.mp3")
bgm = AudioSegment.from_mp3("bgm.mp3")

# BGM 音量降至 10%（-20dB）
bgm = bgm - 20

# 循环 BGM 至与语音等长
while len(bgm) < len(voice):
    bgm = bgm + bgm

bgm = bgm[:len(voice)]

# 混合
mixed = voice.overlay(bgm)
mixed.export("output_with_bgm.mp3", format="mp3", bitrate="192k")
```

### 输出格式规范

| 格式 | 参数 | 适用场景 |
|------|------|---------|
| MP3 | 192kbps, 44.1kHz, stereo | 通用发布（推荐）|
| WAV | 44.1kHz, 16bit, stereo | 专业后期处理 |
| M4A | 128kbps AAC | 苹果生态发布 |
| OGG | 160kbps Vorbis | 网页播放 |

### ffmpeg 格式转换

```bash
# MP3 (192kbps)
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# WAV (高质量)
ffmpeg -i input.mp3 -ar 44100 -ac 2 -acodec pcm_s16le output.wav

# M4A (AAC)
ffmpeg -i input.mp3 -codec:a aac -b:a 128k output.m4a
```

### 静音检测与分段

```python
from pydub.silence import split_on_silence

chunks = split_on_silence(
    audio,
    min_silence_len=500,    # 最小静音时长 500ms
    silence_thresh=-40,      # 静音阈值 -40dBFS
    keep_silence=300         # 保留 300ms 静音边界
)
```
