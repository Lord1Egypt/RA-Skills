---
name: create-video
version: "1.0.0"
description: 视频生成工具。当用户说"CreateVideo"、"创建视频"、"生成视频"或提供文案要求制作视频时触发。支持文本转语音（通过 ListenHub MCP）、模版视频裁剪合并、内容分析输出。依赖 ffmpeg 和 ListenHub MCP Server。
---

# CreateVideo Skill

## 功能说明

将音频或文本转化为带背景音乐的竖屏视频。

**支持两种输入模式：**
- **模式A**：用户直接提供音频文件（MP3）
- **模式B**：用户提供文本文案，系统自动调用 TTS 生成音频

## 工作流程

### 步骤1：接收输入

用户提供以下任一：
- **音频文件**：MP3/WAV 格式的配音
- **文本文案**：需要转化为语音的文案内容

### 步骤2：创建任务目录

```bash
DATE=$(date +%Y%m%d)
BASE_DIR="{{skills_dir}}/../video-projects"
TASK_DIR="$BASE_DIR/${DATE}_001"

COUNTER=1
while [ -d "$TASK_DIR" ]; do
  COUNTER=$((COUNTER + 1))
  TASK_DIR="$BASE_DIR/${DATE}_$(printf "%03d" $COUNTER)"
done

mkdir -p "$TASK_DIR/temp"
```

> `{{skills_dir}}` 为 skill 所在目录，安装后会自动替换为实际路径。

### 步骤3：准备视频模版

将背景视频放入 `video-projects/` 目录（建议 720×1280 竖屏，MP4 格式）。

推荐模版来源（免费素材）：
- Pexels / Pixabay 的竖屏视频
- 自己拍摄的背景视频

### 步骤4：获取音频（二选一）

#### 模式A：用户提供音频文件

将用户发来的音频文件保存到 `$TASK_DIR/voice.mp3`。

#### 模式B：文本转语音（TTS）

调用 ListenHub MCP 的 `create_flowspeech` 接口：

```
工具：create_flowspeech
参数：
  - sourceType: "text"
  - sourceContent: 用户文案
  - speakerId: 用户指定的音色ID（在 ListenHub 音色库中选择）
  - language: "zh"
  - mode: "smart"
```

> 首次使用前，用户需在 ListenHub 音色库中选择自己喜好的音色，复制其 ID 后使用。

### 步骤5：合并视频与音频

```bash
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TASK_DIR/voice.mp3")

ffmpeg -y \
  -stream_loop 3 -i "$TASK_DIR/template.mp4" \
  -i "$TASK_DIR/voice.mp3" \
  -t $DURATION \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -map 0:v:0 -map 1:a:0 \
  "$TASK_DIR/output.mp4"
```

说明：
- `-stream_loop 3` 表示循环4次，根据音频长度调整
- 模版视频时长应足够覆盖音频长度，或使用 `math.ceil(DURATION/TEMPLATE_DUR)` 计算循环次数
- 如服务器不支持 libx264 编码，可使用 `-c:v copy` 直接复制原视频流

### 步骤6：生成内容分析（仅模式B需要）

基于原始文案生成并保存到 `$TASK_DIR/内容分析.txt`：
1. **核心金句** — 最具传播力的一句话
2. **洞见** — 深层洞察和价值点
3. **内容描述** — 50字概括视频核心内容
4. **朋友圈文案** — 200字推广文案

### 步骤7：输出结果

```
**视频创建完成！**

**任务目录**: {路径}
**最终视频**: output.mp4

**音频来源**: {TTS合成 / 用户音频}
**时长**: {时长}
```

## 默认配置

| 配置项 | 说明 |
|--------|------|
| 基础目录 | `{skills_dir}/../video-projects` |
| 模版目录 | `video-projects/` |
| 音频文件 | `voice.mp3` |
| 输出文件 | `output.mp4` |

## 目录结构

```
video-projects/
├── v_template.mp4      # 背景视频模版（需用户自行准备）
├── 20260411_001/
│   ├── voice.mp3       # 配音音频
│   ├── template.mp4    # 复制的模版
│   └── output.mp4      # 最终视频
└── temp/               # 临时文件（可定期清理）
```

## 依赖

- **ffmpeg / ffprobe** — 系统安装，视频处理
- **ListenHub MCP Server** — TTS 语音合成（如使用模式B）

## ListenHub 安装配置（模式B必需）

### 1. 安装 MCP Server

```bash
npx -y @marswave/listenhub-mcp-server
```

### 2. 配置到 OpenClaw

在 OpenClaw 配置中添加 MCP Server 连接。

### 3. 获取音色

调用 `get_speakers` 工具（language=zh）查看可用音色列表，选择音色后复制其 ID。

## 注意事项

1. 模版视频需用户自行准备，建议使用竖屏（9:16）格式
2. 模版视频放入 `video-projects/` 目录即可被自动使用
3. 每次任务自动创建日期序号目录
4. 中间文件在 `temp/` 子目录，可定期清理
5. 如服务器不支持视频编码，可使用 `-c:v copy` 模式（需要模版视频编码格式兼容）
