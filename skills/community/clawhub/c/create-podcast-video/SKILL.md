---
name: create-video
description: 视频生成工具。当用户说"CreateVideo"、"创建视频"、"生成视频"或提供文案要求制作播客视频时触发。支持双人播客音频生成（通过 ListenHub MCP）、模版视频裁剪合并、内容分析输出。依赖 ffmpeg 和 ListenHub MCP Server。
---

# CreateVideo Skill

## 工作流程

### 1. 接收输入

用户提供：
- **必须**：视频文案内容
- **可选**：模版选择（默认根据文案内容自动选择）
  - `书房` / `夜景` → `$BASE_DIR/v_template.mp4`（上海夜景书房，29.6s）
  - `能量` / `能量人` → `$BASE_DIR/v_template_energy.mov`（能量人，14.7s）

### 2. 创建任务目录

```bash
DATE=$(date +%Y%m%d)
BASE_DIR="/root/.openclaw/workspace/video-projects"
TASK_DIR="$BASE_DIR/${DATE}_001"

COUNTER=1
while [ -d "$TASK_DIR" ]; do
  COUNTER=$((COUNTER + 1))
  TASK_DIR="$BASE_DIR/${DATE}_$(printf "%03d" $COUNTER)"
done

mkdir -p "$TASK_DIR/temp"
```

### 3. 复制模板视频

根据文案内容或用户指定选择模版：

```bash
# 自动选择逻辑：能量/潜意识/吸引力类 → 能量人模版，其他 → 书房夜景模版
# 用户也可以直接指定："用能量人模版" / "用书房模版"
cp "$BASE_DIR/v_template.mp4" "$TASK_DIR/template.mp4"        # 书房夜景（默认）
# 或
cp "$BASE_DIR/v_template_energy.mov" "$TASK_DIR/template.mp4"  # 能量人
```

### 4. 生成双人播客音频（ListenHub MCP）

通过 ListenHub MCP 生成双人播客音频：

1. 调用 `create_podcast`：
   - `query`: 用户文案内容
   - `speakerIds`: ["YOUR_SPEAKER_ID_1", "YOUR_SPEAKER_ID_2"]（主播A先说，主播B后说）
   - `language`: "zh"
   - `mode`: "quick"
4. 等待生成完成，下载音频到 `$TASK_DIR/podcast_audio.mp3`

> 详细 MCP 参数参见 [references/listenhub-guide.md](references/listenhub-guide.md)

### 5. 无缝循环模版视频（stream_loop）

使用 ffmpeg 的 `stream_loop` 实现无缝循环，一步完成循环+音频合并+输出：

> ⚠️ **不要用 concat demuxer + 正放↔倒放方案**，会在接缝处冻帧（2026-03-22 踩坑验证）

```bash
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TASK_DIR/podcast_audio.mp3")
TEMPLATE_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TASK_DIR/template.mp4")
LOOPS=$(python3 -c "import math; print(math.ceil($DURATION / $TEMPLATE_DUR))")

TITLE="根据文案内容生成的标题"

ffmpeg -y -stream_loop $LOOPS -i "$TASK_DIR/template.mp4" \
  -i "$TASK_DIR/podcast_audio.mp3" \
  -t $DURATION \
  -c:v libx264 -preset fast -b:v 1400k \
  -c:a aac -map 0:v:0 -map 1:a:0 \
  "$TASK_DIR/${TITLE}.mp4"
```

说明：
- `stream_loop` 直接循环原始模版，无接缝问题
- `-b:v 1400k` 控制输出大小（720×1280 竖屏约 40MB/4min）
- 一条命令同时完成：循环视频 + 合并音频 + 裁剪时长 + 输出最终文件
- 不再需要中间文件（trimmed.mp4、merged.mp4、template_reversed.mp4）

### 6. 生成内容分析

基于原始文案和播客脚本，生成并保存到 `$TASK_DIR/内容分析.txt`：

1. **核心金句** — 最具传播力的一句话
2. **洞见** — 深层洞察和价值点
3. **内容描述** — 50字概括视频核心内容
4. **朋友圈文案** — 200字推广文案

### 7. 输出结果格式

```
**视频创建完成！**

**任务目录**: {路径}
**最终视频**: {文件名}

**播客信息**:
- 标题: {标题}
- 音色: 主播A + 主播B
- 时长: {时长}

---

**内容分析**:

核心金句：...
洞见：...
内容描述（50字）：...
朋友圈文案（200字）：...
```

## 任务目录结构

```
video-projects/20260322_001/
├── template.mp4          # 复制的模版视频
├── temp/                 # 临时中间文件（可清理）
├── podcast_audio.mp3     # 播客音频
├── {标题}.mp4            # 最终视频
└── 内容分析.txt          # 内容分析
```

## 默认配置

| 配置项 | 默认值 |
|--------|--------|
| 基础目录 | `/root/.openclaw/workspace/video-projects` |
| 模版视频A | `v_template.mp4`（720×1280，29.6s，上海夜景书房）— 认知/读书/财富类 |
| 模版视频B | `v_template_energy.mov`（720×1280，14.7s，能量人）— 能量/潜意识/吸引力类 |
| 播客音色1（先说） | 主播A（`YOUR_SPEAKER_ID_1`，在 ListenHub 获取） |
| 播客音色2（后说） | 主播B（`YOUR_SPEAKER_ID_2`，在 ListenHub 获取） |
| 播客模式 | quick（3-5分钟） |
| 播客语言 | zh（中文） |

## 依赖

- `ffmpeg` / `ffprobe` — 视频处理
- ListenHub MCP Server — `@marswave/listenhub-mcp-server`（需要 LISTENHUB_API_KEY）

## 安装配置

### 1. 安装 ListenHub MCP
```bash
claude mcp add listenhub --env LISTENHUB_API_KEY=<你的API Key> -- npx -y @marswave/listenhub-mcp-server
```
API Key 在 [ListenHub 官网](https://marswave.ai) 注册后获取。

### 2. 配置音色 ID
在使用前，先调用 `get_speakers` 查询可用音色，将你选择的音色 ID 填入 Skill 配置：
- `YOUR_SPEAKER_ID_1` — 主播A（先说）
- `YOUR_SPEAKER_ID_2` — 主播B（后说）

### 3. 准备模版视频
将你的背景视频放入 `video-projects/` 目录：
- `v_template.mp4` — 默认模版（720×1280 竖屏）
- `v_template_energy.mov` — 备选模版（可选）

## 注意事项

1. 播客音频生成需要几分钟，耐心等待
2. 每次任务自动创建日期序号目录（如 `20260321_001`）
3. 中间文件在 `temp/` 子目录，可手动清理
4. 模板文件复制到任务目录，不影响原始文件
