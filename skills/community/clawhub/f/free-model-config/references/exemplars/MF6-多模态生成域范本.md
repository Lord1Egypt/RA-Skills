# MF6 多模态生成域范本

## 范本说明

本范本提供多模态生成的完整流程示例，包括图像生成、视频生成、音频生成、TTS配音和音视频合并。

---

## 1. 图像生成范本（MF6-01）

### 输入
- 提示词：一群人在王太平面前跪拜
- 分辨率：1024x768
- 输出：output.png

### 执行命令
```bash
python agnes_gen.py image --prompt "A group of people kneeling before Wang Taiping" --size 1024x768 --output output.png
```

### 输出
- 图像文件：output.png

---

## 2. 视频生成范本（MF6-02）

### 输入
- 提示词：一群人在王太平面前跪拜，狂热激动
- 分辨率：1088x832（720p）
- 帧数：121帧
- 帧率：24fps
- 输出：output.mp4

### 执行命令
```bash
python agnes_gen.py video --prompt "A group of people kneeling before Wang Taiping, fervent worship" --width 1088 --height 832 --frames 121 --fps 24 --output output.mp4
```

### 输出
- 视频文件：output.mp4（约5秒）

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
- 文本：王太平
- 声音：zh-CN-YunxiNeural（年轻男声）
- 输出：speech.mp3

### 执行命令
```bash
python generate_tts_audio.py --text "王太平" --voice zh-CN-YunxiNeural --output speech.mp3
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
生成一个"一群人狂热跪拜王太平"的视频，带配音。

### 步骤

1. **生成图像**
```bash
python agnes_gen.py image --prompt "A group of people kneeling before Wang Taiping, fervent worship" --output anchor.png
```

2. **生成视频**
```bash
python agnes_gen.py video --prompt "A group of people kneeling before Wang Taiping, fervent worship" --width 1088 --height 832 --frames 121 --fps 24 --output video.mp4
```

3. **生成配音**
```bash
python generate_tts_audio.py --text "王太平！王太平！" --voice zh-CN-YunxiNeural --output speech.mp3
```

4. **合并音视频**
```bash
python merge_audio_video.py --video video.mp4 --audio speech.mp3 --output final.mp4 --mode replace
```

### 输出
- 最终视频：final.mp4（带配音的跪拜视频）

---

## 注意事项

1. **视频生成时间**：视频生成需要3-10分钟，请耐心等待
2. **帧数限制**：帧数按分辨率受限，需满足8n+1格式
3. **图片上传**：图片上传可能失败，备选方案是直接从文本生成视频
4. **TTS安装**：需要先安装edge-tts：`pip install edge-tts`
5. **ffmpeg要求**：音视频合并需要ffmpeg工具