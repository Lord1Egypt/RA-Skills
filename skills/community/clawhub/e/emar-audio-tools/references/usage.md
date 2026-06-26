# Audio Tools 使用文档

## 环境检查

执行任何命令前，建议先检查环境依赖：

```bash
# 检查环境状态
python D:\workbuddy\skills\audio-tools\scripts\audio_tools.py --check
```

输出示例：
```
==================================================
Audio Tools - Environment Check
==================================================
[OK] Python 3.10.11
[OK] ffmpeg (bundled): D:\workbuddy\skills\audio-tools\bin\ffmpeg.exe
[OK] ffprobe (bundled): D:\workbuddy\skills\audio-tools\bin\ffprobe.exe
[OK] ffplay (bundled): D:\workbuddy\skills\audio-tools\bin\ffplay.exe
[--] moviepy: not installed (auto-install on first use)
[--] openai-whisper: not installed (auto-install on first use)
==================================================
```

**环境要求**：
- Python 3.8 或更高版本
- ffmpeg（推荐）或 moviepy（备选）

如果缺少依赖，脚本会给出清晰的安装指引。

---

## 环境准备

### 方式一：Bundled ffmpeg（推荐）
将 ffmpeg 放入 Skill 的本地 bin 目录，实现零依赖、开箱即用：

```
D:\workbuddy\skills\audio-tools\
└── bin\
    ├── ffmpeg.exe      ← 音视频处理
    ├── ffprobe.exe     ← 可选，查时长用
    └── ffplay.exe      ← 可选，播放用
```

**获取 ffmpeg**：
1. 从 https://ffmpeg.org/download.html 下载 Windows 版本
2. 解压后将 `ffmpeg.exe`、`ffprobe.exe`、`ffplay.exe` 放入 `bin/` 目录

**工具查找优先级**：
- 提取/截取：**本地 bin/ffmpeg > 系统 PATH > moviepy**
- 播放：**本地 bin/ffplay > 系统默认播放器**

---

### 方式二：系统 ffmpeg
如果希望使用系统全局安装的 ffmpeg：

**Windows 安装**：
```powershell
# 方法1：winget（推荐）
winget install ffmpeg

# 方法2：手动下载
# 访问 https://ffmpeg.org/download.html 下载 Windows 版本
# 解压后将 bin 目录路径（如 C:\ffmpeg\bin）添加到系统 PATH

# 验证安装
ffmpeg -version
```

---

### 方式三：moviepy（备选）
如果没有 ffmpeg，脚本会自动安装 moviepy 作为备选：
```bash
pip install moviepy
```

---

## 脚本直接调用

脚本位置：`D:\workbuddy\skills\audio-tools\scripts\audio_tools.py`

### 1. 提取音频

```bash
# 基础用法（输出到同目录，同名 .wav）
python audio_tools.py extract --input "D:\workbuddy\video.mp4"

# 指定输出路径
python audio_tools.py extract --input "D:\workbuddy\video.mp4" --output "D:\workbuddy\output.wav"

# 简写参数
python audio_tools.py extract -i video.mp4 -o output.wav
```

### 2. 截取音频片段

```bash
# 从第30秒开始，截取60秒
python audio_tools.py clip --input "D:\workbuddy\audio.wav" --start 30 --duration 60

# 使用时间格式（HH:MM:SS）
python audio_tools.py clip --input "D:\workbuddy\audio.wav" --start 00:00:30 --duration 60

# 指定输出路径
python audio_tools.py clip -i audio.wav -s 30 -d 60 -o "D:\workbuddy\clip.wav"
```

### 3. 播放媒体文件

**播放工具优先级**：ffplay（bundled）> 系统默认播放器

```bash
# 播放视频（优先使用 ffplay，显示画面）
python audio_tools.py play --input "D:\workbuddy\video.mp4"

# 播放音频（优先使用 ffplay，无画面模式）
python audio_tools.py play --input "D:\workbuddy\audio.wav"
```

**说明**：
- 如果 `bin/ffplay.exe` 存在，使用 ffplay 播放（格式支持最全）
- 如果 ffplay 不存在，自动回退到系统默认播放器
- ffplay 播放完会自动退出（`-autoexit` 参数）

### 4. 语音识别转文字（Whisper）

使用 OpenAI Whisper 将音频/视频中的语音转为文字，输出 JSON 格式。

```bash
# 基础用法（自动检测语言，使用 small 模型）
python audio_tools.py transcribe --input "D:\workbuddy\lecture.wav"

# 指定语言和模型
python audio_tools.py transcribe -i lecture.wav -m small -l zh

# 指定输出路径
python audio_tools.py transcribe -i lecture.wav -o result.json
```

**模型大小对照**：
| 模型 | 大小 | 速度 | 适用场景 |
|------|------|------|---------|
| `tiny` | 39M | 最快 | 实时、测试 |
| `base` | 74M | 快 | 快速处理 |
| `small` | 244M | 中等 | **推荐，平衡准确度和速度** |
| `medium` | 769M | 慢 | 高精度需求 |
| `large` | 1550M | 最慢 | 最高精度 |

**语言代码**：`zh`(中文), `en`(英文), `ja`(日文), `ko`(韩文), `fr`(法文) 等，默认自动检测。

**输出文件**：
- `同名.json` - 完整数据（文字、时间戳、置信度）
- `同名.txt` - 纯文本文字

### 5. 提取音频/视频元数据

查看文件的详细信息：时长、码率、编码、采样率等。

```bash
# 终端输出元数据
python audio_tools.py metadata --input "D:\workbuddy\video.mp4"

# 保存到 JSON 文件
python audio_tools.py metadata -i audio.wav -o meta.json
```

**输出信息**：文件大小、时长、码率、音频编码、采样率、声道数、视频分辨率、帧率等。

---

## 参数速查表

### extract（提取音频）
| 参数 | 简写 | 必填 | 说明 | 示例 |
|------|------|:----:|------|------|
| `--input` | `-i` | ✅ | 输入视频文件 | `video.mp4` |
| `--output` | `-o` | ❌ | 输出WAV路径 | `output.wav` |

### clip（截取片段）
| 参数 | 简写 | 必填 | 说明 | 示例 |
|------|------|:----:|------|------|
| `--input` | `-i` | ✅ | 输入音频文件 | `audio.wav` |
| `--start` | `-s` | ✅ | 开始时间 | `30` 或 `00:00:30` |
| `--duration` | `-d` | ✅ | 截取时长（秒） | `60` |
| `--output` | `-o` | ❌ | 输出路径 | `clip.wav` |

### play（播放）
| 参数 | 简写 | 必填 | 说明 | 示例 |
|------|------|:----:|------|------|
| `--input` | `-i` | ✅ | 媒体文件路径 | `video.mp4` |

### transcribe（语音识别）
| 参数 | 简写 | 必填 | 说明 | 示例 |
|------|------|:----:|------|------|
| `--input` | `-i` | ✅ | 输入音频/视频 | `audio.wav` |
| `--output` | `-o` | ❌ | 输出JSON路径 | `result.json` |
| `--model` | `-m` | ❌ | 模型：`tiny/base/small/medium/large` | `small` |
| `--language` | `-l` | ❌ | 语言代码 | `zh`, `en` |

### metadata（元数据）
| 参数 | 简写 | 必填 | 说明 | 示例 |
|------|------|:----:|------|------|
| `--input` | `-i` | ✅ | 输入文件路径 | `video.mp4` |
| `--output` | `-o` | ❌ | 输出JSON路径（默认终端输出） | `meta.json` |

---

## 支持的文件格式

### 输入格式
| 类型 | 支持格式 |
|------|---------|
| 视频 | mp4, mkv, avi, mov, flv, wmv, m4v, webm |
| 音频 | wav, mp3, flac, aac, m4a, ogg, wma |

### 输出格式
- 提取音频：始终输出 **WAV**（PCM 16bit, 44100Hz, 立体声）
- 截取片段：默认输出 **WAV**，可通过 `--output` 指定其他格式

---

## 常见问题

**Q：提示 `ffmpeg` 未找到怎么办？**
A：安装 ffmpeg 并确保其加入 PATH，或直接运行脚本，会自动使用 moviepy。

**Q：截取时长超过文件实际时长会报错吗？**
A：不会报错，moviepy 模式下会自动截到文件末尾。ffmpeg 模式下同样会静默处理。

**Q：路径有中文或空格怎么办？**
A：用引号包裹路径即可，如 `--input "D:\我的视频\test video.mp4"`

**Q：如何截取到文件末尾（不知道确切时长）？**
A：可以先用 ffmpeg 查询时长：
```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 "input.mp4"
```

---

## 工作目录说明

默认工作目录为 `D:\workbuddy`。当你输入不带盘符的相对路径时，脚本会自动补全：
- 输入：`video.mp4` → 实际路径：`D:\workbuddy\video.mp4`
- 输入：`output\result.wav` → 实际路径：`D:\workbuddy\output\result.wav`

如需使用其他目录，直接输入完整绝对路径即可。
