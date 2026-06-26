# bili-summary

Bilibili 视频文本提取与 AI 总结工具。

一个字幕/音频转写 + 弹幕 + 评论的全方位提取工具，输出结构化数据供任何 AI Agent（或人类）进行深度总结。

## 它能做什么

给定一个 B 站视频链接，自动完成：

| 数据源 | 方式 | 说明 |
|--------|------|------|
| **CC 字幕** | B 站 API | 如果有字幕直接获取，最快 |
| **语音转写** | whisper.cpp + Vulkan GPU | 无字幕时自动走音频转写，支持 AMD/NVIDIA GPU |
| **视频简介** | yt-dlp | 标题、UP 主、时长、简介文本 |
| **弹幕** | yt-dlp | 下载弹幕 XML，分析高频弹幕和内容分布 |
| **评论** | B 站评论 API | 抓取热评，按点赞排序，含子回复 |

所有数据输出为 JSON，**不依赖任何外部 AI API**（不需要 OpenAI/Gemini key）。

## 快速开始

### 安装依赖

```bash
pip install yt-dlp av
```

### 下载 whisper.cpp（可选，用于语音转写）

如果视频没有 CC 字幕，需要 GPU 转写：

1. 从 [whisper.cpp releases](https://github.com/ggerganov/whisper.cpp/releases) 下载对应系统的版本
2. 确保你的 GPU 支持 Vulkan（Linux/NVIDIA/AMD 均可）
3. 下载模型文件（如 `ggml-large-v3-turbo.bin`）
4. 将 whisper-cli 和模型放在本仓库的 `whisper-cpp/` 目录下（或用环境变量指定路径）

也可以直接用系统路径中的 `whisper-cli`。

### 使用

```bash
# 一步到位：转写 + 弹幕 + 评论
python bili-transcript.py "https://www.bilibili.com/video/BV1kqdxBEEoe"

# 只看基本信息
python bili-transcript.py "https://www.bilibili.com/video/BV1kqdxBEEoe" --action info

# 只抓弹幕
python bili-transcript.py "https://www.bilibili.com/video/BV1kqdxBEEoe" --action danmaku

# 只抓评论
python bili-transcript.py "https://www.bilibili.com/video/BV1kqdxBEEoe" --action comments

# 强制 GPU 转写（跳过字幕检测）
python bili-transcript.py "https://www.bilibili.com/video/BV1kqdxBEEoe" --action transcribe

# 指定输出目录
python bili-transcript.py "https://www.bilibili.com/video/BV1kqdxBEEoe" --output ./my-output
```

### 自定义 whisper.cpp 路径

```bash
# 环境变量方式
export WHISPER_CPP_DIR=/path/to/whisper-cpp
export WHISPER_MODEL=/path/to/model.bin
python bili-transcript.py "<URL>"

# 或命令行参数
python bili-transcript.py "<URL>" --whisper-dir /path/to/whisper-cpp --model /path/to/model.bin
```

## 输出结构

`--action text`（默认）输出 JSON，结构如下：

```json
{
  "title": "视频标题",
  "uploader": "UP 主",
  "duration": 327,
  "description": "视频简介（前 500 字）",
  "source": "whisper_gpu | subtitle",
  "char_count": 2304,
  "text_file": "./bili-output/transcript.txt",
  "text_preview": "转写文本前 2000 字...",
  "danmaku": {
    "available": true,
    "count": 51,
    "unique_count": 33,
    "frequent": [{"text": "高频弹幕", "count": 13}, ...],
    "file": "./bili-output/danmaku.json"
  },
  "comments": {
    "available": true,
    "count": 1026,
    "fetched": 57,
    "top_liked": [{"user": "用户名", "message": "高赞评论", "like": 43}, ...],
    "file": "./bili-output/comments.json"
  }
}
```

相关文件也会分别保存到输出目录：
- `transcript.txt` — 完整转写文本
- `danmaku.json` — 弹幕原始数据 + 统计
- `comments.json` — 评论原始数据 + 统计

## 给 AI Agent 的工作流

如果你是 AI Agent，想要用这个工具做 B 站视频总结，推荐的工作流：

### Step 1: 提取数据

```bash
python bili-transcript.py "<URL>"
```

输出 JSON 包含了预览信息。转写文本完整内容在 `transcript.txt`。

### Step 2: 读取完整文本

```bash
cat ./bili-output/transcript.txt
```

### Step 3: 读取弹幕和评论

```bash
cat ./bili-output/danmaku.json
cat ./bili-output/comments.json
```

### Step 4: 综合总结

拿到所有数据后，建议按以下结构组织总结：

- **视频概览**：标题、UP 主、时长、转写来源。简介中的项目链接和关键信息也应提及。
- **核心内容**：视频主要讲了什么，流畅的段落概括。
- **关键观点**：值得注意的论点、数据、信息点。
- **社区反应**（可选）：弹幕和评论中的讨论热点、高赞观点、争议点。如果无实质内容则跳过。
- **评价**（可选）：内容质量、信息密度、亮点。

弹幕分析关注：高频弹幕反映的集体反应、有信息量的提问或补充、争议点。
评论分析关注：高赞观点、UP 主互动、用户反馈的问题和建议、技术讨论。

## 依赖

- **Python >= 3.9**
- **yt-dlp** — 视频信息获取、音频下载、弹幕下载
- **av (PyAV)** — 音频格式转换（m4a → wav）
- **whisper.cpp**（可选）— GPU 加速语音转写
- 无需任何外部 AI API key

## 局限

- 需要网络访问 B 站
- 部分内容需要登录（付费课程、限制级视频等）
- 弹幕和评论 API 可能受限于登录状态
- 极长视频（>2 小时）转写耗时较长
- 评论默认抓取前 3 页（约 60 条），热门视频可能无法完全覆盖

## License

MIT
