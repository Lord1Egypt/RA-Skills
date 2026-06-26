# Tools Reference - 工具速查表

## FFmpeg 常用命令

### 视频剪切（无损）
```bash
ffmpeg -i input.mp4 -ss 00:01:30 -to 00:02:45 -c copy output.mp4
```

### 视频拼接
```bash
# 创建文件列表 filelist.txt
# file 'part1.mp4'
# file 'part2.mp4'
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4
```

### 添加/替换音频
```bash
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
```

### 调整音量
```bash
ffmpeg -i input.mp4 -af "volume=1.5" output.mp4  # 1.5倍音量
```

### 视频缩放
```bash
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### 提取帧（截图）
```bash
ffmpeg -ss 00:00:05 -i input.mp4 -vframes 1 -q:v 2 output.jpg
```

### 视频信息
```bash
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4
```

## Pillow 常用操作

```python
from PIL import Image, ImageFilter, ImageEnhance

# 打开图片
img = Image.open("input.jpg")

# 缩放
img = img.resize((800, 800), Image.LANCZOS)

# 裁剪 (left, top, right, bottom)
img = img.crop((0, 0, 400, 400))

# 格式转换
img.save("output.png", "PNG")
img.save("output.webp", "WEBP", quality=85)

# 调整亮度
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.2)  # 1.0 = original

# 调整对比度
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.15)

# 调整锐度
enhancer = ImageEnhance.Sharpness(img)
img = enhancer.enhance(1.5)

# 合成图片（叠加透明PNG到背景）
background = Image.open("bg.jpg").convert("RGBA")
overlay = Image.open("logo.png").convert("RGBA")
background.paste(overlay, (100, 100), overlay)
background.save("composite.png")
```

## rembg 抠图模型

| 模型 | 速度 | 质量 | 适用场景 |
|------|------|------|---------|
| u2net | 中 | 高 | 通用产品图（默认） |
| u2net_human_seg | 中 | 高 | 人像 |
| isnet-general-use | 慢 | 最高 | 高精度产品图 |
| silueta | 快 | 中 | 简单物体 |

命令行：
```bash
rembg i -m u2net input.jpg output.png
rembg i -m isnet-general-use -a input.jpg output.png  # -a = alpha matting
```

## edge-tts 中文语音

| 语音名称 | 性别 | 风格 |
|---------|------|------|
| zh-CN-XiaoxiaoNeural | 女 | 自然、温暖（默认） |
| zh-CN-YunxiNeural | 男 | 专业、沉稳 |
| zh-CN-XiaoyiNeural | 女 | 活泼、年轻 |
| zh-CN-YunjianNeural | 男 | 成熟、大气 |
| zh-CN-YunyangNeural | 男 | 新闻播报风格 |
| zh-CN-XiaochenNeural | 女 | 客服/讲解风格 |

命令行：
```bash
edge-tts --voice zh-CN-XiaoxiaoNeural --text "萤火虫空压机，专注节能十五年" --write-media output.mp3
edge-tts --voice zh-CN-XiaoxiaoNeural -f text.txt --write-media output.mp3
```

英语语音：
```bash
edge-tts --voice en-US-JennyNeural --text "Firefly Air Compressor, energy saving experts" --write-media output.mp3
```

## easyocr 常用参数

```python
import easyocr

# 中英文混合识别
reader = easyocr.Reader(['ch_sim', 'en'])
results = reader.readtext('image.jpg')
# results: [(bbox, text, confidence), ...]

# 只识别英文（更快）
reader = easyocr.Reader(['en'])
results = reader.readtext('image.jpg')
```
