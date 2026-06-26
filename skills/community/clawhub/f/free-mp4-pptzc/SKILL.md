# Presentation Video Maker

将PPT演示文稿自动转换为带讲解配音的视频。

## 适用场景

- 工作汇报视频
- 项目成果展示
- 教程/培训视频
- 产品演示
- 任何需要"幻灯片+语音讲解"的场景

## 快速开始

### 方式一：纯文本脚本（推荐）

创建脚本文件，格式如下：
```
# 幻灯片标题
内容要点1
内容要点2

# 下一页标题
更多内容...
```

### 方式二：HTML模板（更精美）

使用HTML模板生成更专业的幻灯片，支持：
- 🎨 精美图标（FontAwesome）
- 🌈 渐变背景与装饰元素
- ✨ CSS动画效果
- 📐 灵活布局（Flex/Grid）

模板类型：
- `cover` - 封面页（带图标、渐变）
- `content` - 内容页（列表、子列表）
- `dual` - 双栏对比页
- `timeline` - 时间线页
- `ending` - 结束页

### 调用技能

```
请帮我制作一个演示视频：
- 脚本：[提供内容]
- 模式：[文本/HTML模板]
- 配音：[中文/英文]
```

## 完整流程

### Step 1: 生成幻灯片图片

**方法A：从PPT转换（推荐）**
```bash
# 使用python-pptx读取PPT，每张幻灯片保存为图片
python scripts/ppt_to_images.py <input.pptx> <output_dir>
```

**方法B：直接生成图片（适合简单内容）**
```bash
python scripts/create_slides_from_text.py <script.txt> <output_dir>
```

### Step 2: 生成讲解配音

```bash
python scripts/generate_narration.py \
    --text "你的讲解脚本" \
    --voice zh-CN-XiaoxiaoNeural \
    --rate +5% \
    --output narration.mp3
```

**可用语音列表：**

| 语言 | 语音 | 风格 |
|------|------|------|
| 中文 | zh-CN-XiaoxiaoNeural | 女声，自然流畅（默认） |
| 中文 | zh-CN-YunxiNeural | 男声，自然 |
| 中文 | zh-CN-YunyangNeural | 男声，播报风格 |
| 英文 | en-US-MichelleNeural | 女声，自然 |
| 英文 | en-US-GuyNeural | 男声，自然 |

### Step 3: 合成视频

```bash
python scripts/synthesize_video.py \
    --slides <output_dir> \
    --audio narration.mp3 \
    --output final_video.mp4
```

## 脚本说明

### make_video.py（文本模式）

从纯文本脚本生成幻灯片图片并合成视频。

```bash
python make_video.py script.txt output.mp4
```

### make_video_html.py（HTML模板模式）

使用HTML模板生成精美幻灯片。

```bash
python make_video_html.py script.txt output.mp4 --install-playwright
```

**脚本格式（支持类型标记）：**
```
# 封面
type: cover

# 内容页
type: content
- 要点1
- 要点2

# 双栏对比
type: dual
左栏内容
右栏内容

# 时间线
type: timeline
事件1
事件2

# 结束页
type: ending
```

### create_slides_from_text.py

从纯文本脚本生成幻灯片图片。

**输入格式：**
```
# 幻灯片1标题
这是第一页的内容
- 要点1
- 要点2

# 幻灯片2标题
这是第二页的内容
```

### generate_narration.py

使用Edge TTS生成高质量语音。

**参数：**
- `--text`: 讲解脚本（支持多段落）
- `--voice`: 语音名称
- `--rate`: 语速调整（+5% 表示稍快）
- `--pitch`: 音调调整
- `--output`: 输出文件

### synthesize_video.py

将幻灯片图片与音频合成为视频。

**参数：**
- `--slides`: 幻灯片图片目录
- `--audio`: 配音音频文件
- `--output`: 输出视频路径
- `--fps`: 帧率（默认25）
- `--resolution`: 分辨率（1920x1080默认）

## 示例：完整制作流程

```bash
# 1. 创建幻灯片
python create_slides_from_text.py script.txt slides/

# 2. 生成配音
python generate_narration.py --text "欢迎观看..." --output narration.mp3

# 3. 合成视频
python synthesize_video.py --slides slides/ --audio narration.mp3 --output demo.mp4
```

## 输出文件

| 文件 | 说明 |
|------|------|
| `slides/slide_01.png` | 幻灯片图片 |
| `narration.mp3` | 讲解配音 |
| `demo.mp4` | 最终视频（MP4格式） |

## 依赖安装

### 基础依赖（文本模式）
```bash
pip install python-pptx pillow edge-tts
```

### HTML模板模式额外依赖
```bash
pip install playwright
python -m playwright install chromium
```

### ffmpeg（视频合成）
- Windows: `winget install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `apt install ffmpeg`

## 高级用法

### 自定义每页显示时长

```python
# 在 synthesize_video.py 中设置
slide_durations = [5, 10, 15, 8, 10]  # 每页秒数
```

### 添加转场效果

```bash
# ffmpeg 添加淡入淡出
ffmpeg -i slide.png -vf "fade=t=in:st=0:d=0.5" output.png
```

### 添加背景音乐

```bash
ffmpeg -i slides.mp4 -i background.mp3 \
    -filter_complex "[1:a]volume=0.3[a1];[0:a][a1]amix=inputs=2:duration=first" \
    output.mp4
```

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 字体不显示 | 检查字体路径，Windows用msyh.ttc |
| 音频生成失败 | 检查网络连接（Edge TTS需要联网） |
| 视频合成失败 | 确认ffmpeg已安装且路径正确 |
| 幻灯片空白 | 检查文本编码（需UTF-8） |

---

**版本**: 1.0  
**作者**: SenseNova  
**创建日期**: 2026-05-04