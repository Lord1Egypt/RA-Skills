# MF6 多模态生成域范本

## 范本说明

本范本提供多模态生成的完整流程示例，包括图像生成、视频生成、音频生成、TTS配音和音视频合并。

> 基线：Agnes AI Image 2.5 Flash / Video 2.5。视频参数以「秒 + 分辨率档位」表达，旧的帧数参数已废弃。

---

## 1. 图像生成范本（MF6-01）

### 输入
- 提示词：一群人在舞台上欢呼庆祝
- 分辨率档位：2K，画幅 16:9
- 输出：output.png

### 执行命令
```bash
python agnes_gen.py image --prompt "A group of people cheering joyfully on a stage" --size 2K --ratio 16:9 --output output.png
```

### 输出
- 图像文件：output.png（约 2624×1472）

---

## 2. 视频生成范本（MF6-02）

### 输入
- 提示词：一群人在舞台上欢呼庆祝，热情洋溢
- 分辨率档位：720P（免费通道）
- 时长：8 秒
- 画幅：16:9
- 输出：output.mp4

### 执行命令
```bash
python agnes_gen.py video --prompt "A group of people cheering joyfully on a stage, confetti falling, lively atmosphere" --seconds 8 --size 720P --aspect-ratio 16:9 --model agnes-video-2.5-flash --output output.mp4
```

### 输出
- 视频文件：output.mp4（8 秒，720P）

### 变体：首尾帧控制
```bash
python agnes_gen.py video --prompt "The person turns from the first-frame pose and walks toward the window" --image https://example.com/first.png --first-frame https://example.com/first.png --last-frame https://example.com/last.png --seconds 5 --size 1080P --output kf.mp4
```

---

## 3. 视频拼接范本（MF6-03）

### 输入
- 视频文件：video1.mp4, video2.mp4
- 输出：long.mp4

### 执行命令
```bash
python agnes_gen.py concat --inputs video1.mp4 video2.mp4 --output long.mp4
```

### 输出
- 拼接视频：long.mp4

---

## 4. 音频生成范本（MF6-04）

### 输入
- 时长：5秒
- 频率：200,400,600,800 Hz
- 振幅：0.3,0.2,0.15,0.1
- 输出：shout.wav

### 执行命令
```bash
python generate_audio.py --output shout.wav --duration 5.0 --frequencies 200,400,600,800 --amplitudes 0.3,0.2,0.15,0.1
```

### 输出
- 音频文件：shout.wav

---

## 5. TTS配音范本（MF6-05）

### 输入
- 文本：你好，欢迎使用语音合成
- 声音：zh-CN-YunxiNeural（年轻男声）
- 输出：speech.mp3

### 执行命令
```bash
python generate_tts_audio.py --text "你好，欢迎使用语音合成" --voice zh-CN-YunxiNeural --output speech.mp3
```

### 输出
- 语音文件：speech.mp3

---

## 6. 音视频合并范本（MF6-06）

### 输入
- 视频文件：video.mp4
- 音频文件：speech.mp3
- 输出：final.mp4
- 模式：替换原音频

### 执行命令
```bash
python merge_audio_video.py --video video.mp4 --audio speech.mp3 --output final.mp4 --mode replace
```

### 输出
- 最终视频：final.mp4（带配音）

---

## 完整流程示例

### 需求
生成一个"一群人在舞台上欢呼庆祝"的视频，带配音。

### 步骤

1. **生成锚点图像**
```bash
python agnes_gen.py image --prompt "A group of people cheering joyfully on a stage, confetti falling" --size 2K --ratio 16:9 --output anchor.png
```

2. **以锚点图为首帧生成视频**
```bash
python agnes_gen.py video --prompt "A group of people cheering joyfully on a stage, confetti falling, lively atmosphere" --image anchor.png --seconds 8 --size 720P --aspect-ratio 16:9 --output video.mp4
```

3. **生成配音**
```bash
python generate_tts_audio.py --text "欢迎！欢迎！" --voice zh-CN-YunxiNeural --output speech.mp3
```

4. **合并音视频**
```bash
python merge_audio_video.py --video video.mp4 --audio speech.mp3 --output final.mp4 --mode replace
```

### 输出
- 最终视频：final.mp4（带配音的庆祝视频）

---

## 注意事项

1. **视频时长**：单段 `seconds` 只能 4–12 秒；更长用 `long-video --segments N --segment-seconds 10` 分段拼接
2. **分辨率档位**：只能传 720P / 1080P / 1K / 2K，传像素值或 width/height 会 400
3. **免费通道**：`agnes-video-2.5-flash`（720P）当前限时免费；`agnes-video-2.5` 按秒计费
4. **轮询**：`GET /agnesapi?video_id=<ID>&model_name=<模型>`，keyframe/reference 模式必须带 model_name
5. **图片上传**：图片必须是公网 URL，上传失败时改用文生视频
6. **TTS安装**：需要先安装 edge-tts：`pip install edge-tts`
7. **ffmpeg要求**：音视频合并需要 ffmpeg 工具
