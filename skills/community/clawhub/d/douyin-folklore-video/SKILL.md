---
name: douyin-folklore-video
description: 抖音民间诡异故事视频生成器。根据用户提供的文案自动生成配音、图片、视频并合成最终视频，支持上传到抖音。触发词：生成抖音视频、民间故事视频、诡异故事视频、AI视频制作。
---

# 抖音民间诡异故事视频生成器

根据用户提供的文案，全自动生成抖音风格的民间诡异故事视频。

## 完整流程

### 1. 获取故事文案
- 必须使用用户提供的文案
- 保存到 `story.txt`

### 2. 生成配音
调用 `scripts/generate_voice.py`：
```bash
python scripts/generate_voice.py <故事文案> <输出目录>
```
- 输出：`voice.wav`
- 返回：配音时长（秒）

### 3. 生成图片
调用 `scripts/generate_images.py`：
```bash
python scripts/generate_images.py <故事文案> <输出目录>
```
- 根据故事生成 5-6 张图片
- 尺寸：720×1280
- 风格：dark horror comic style
- 保存：`img1.png` ~ `imgN.png`

### 4. 生成视频段
调用 `scripts/generate_videos.py`：
```bash
python scripts/generate_videos.py <图片URL列表> <输出目录>
```
- 每段 5 秒
- 按顺序推进（不回退）
- 保存：`v1.mp4` ~ `vN.mp4`

### 5. 视频拼接
```bash
ffmpeg -f concat -safe 0 -i list.txt -c copy video_raw.mp4
```

### 6. 生成同步字幕
调用 `scripts/generate_subtitle.py`：
```bash
python scripts/generate_subtitle.py <配音时长> <故事文案> <输出目录>
```
- 根据配音时长精确计算每句字幕时间
- 输出：`subtitle.srt`

### 7. 视频合成
```bash
# 加字幕
ffmpeg -i video_raw.mp4 -vf "scale=540:960,subtitles=subtitle.srt" -c:v libx264 -crf 23 -an video_sub.mp4

# 加音频
ffmpeg -i video_sub.mp4 -i voice.wav -c:v copy -c:a aac -map 0:v -map 1:a final_video.mp4
```

### 8. 发送给用户审核
用 message 工具发送 `final_video.mp4` 给用户。

### 9. 用户确认"发布"后上传抖音
使用 browser 工具：
- profile: openclaw
- 上传文件到 `C:\Users\SS\AppData\Local\Temp\openclaw\uploads\`
- 找到 `input[type=file]` 元素上传
- 填写标题、描述、话题
- 添加 AI 声明
- 点击发布

## 关键参数

| 参数 | 值 |
|------|-----|
| 配音模型 | qwen3-tts-flash |
| 图片模型 | wan2.6-t2i |
| 视频模型 | wan2.2-kf2v-flash |
| 图片尺寸 | 720×1280 |
| 视频分辨率 | 540×960 |
| 字幕字号 | 12 |
| 视频编码 | H264 |

## 配置信息

见 `references/config.md`：
- API Key
- FTP 服务器信息
- 浏览器配置

## 视频结构规则

**按顺序推进，不回退：**
```
v1: img1 → img2
v2: img2 → img3
v3: img3 → img4
v4: img4 → img5
...
```

**视频时长规则：**
- 配音时长 + 1~2秒 = 视频时长
- 每段视频固定 5 秒
- 根据配音时长计算需要多少段视频

## 注意事项

1. 字幕必须根据配音时长精确计算，确保同步
2. 视频要比配音长 1-2 秒
3. 上传抖音时必须添加 AI 声明
4. 用户确认"发布"后才能点发布按钮