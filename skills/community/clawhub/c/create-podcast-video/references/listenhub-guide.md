# ListenHub MCP 调用指南

## MCP Server

- **包名**: `@marswave/listenhub-mcp-server`
- **环境变量**: `LISTENHUB_API_KEY`
- **Claude Code 安装**: `claude mcp add listenhub --env LISTENHUB_API_KEY=<key> -- npx -y @marswave/listenhub-mcp-server`

## 可用工具

### get_speakers — 查询音色
- `language`（可选）: `zh` 或 `en`
- 返回音色 ID、姓名、语言、性别、试听链接

### create_podcast — 创建播客（一步生成，推荐）
- `query`（可选）: 内容/主题
- `sources`（可选）: 文本/URL 来源数组
- `speakerIds`（必需）: 1-2 个音色 ID 数组
- `language`（可选，默认 en）: `zh` 或 `en`
- `mode`（可选，默认 quick）: `quick`（速听）、`deep`（深度）、`debate`（辩论）
- 自动轮询至完成（可能需要几分钟）

### create_podcast_text_only — 仅生成文本（先审后录第一步）
- 参数同 create_podcast
- `waitForCompletion`（可选，默认 true）

### generate_podcast_audio — 从文本生成音频（先审后录第二步）
- `episodeId`（必需）: 播客 ID
- `customScripts`（可选）: 自定义脚本数组
- `waitForCompletion`（可选，默认 true）

### get_podcast_status — 查询播客状态
- `episodeId`（必需）: 播客 ID

### create_flowspeech — 文本转语音
- `sourceType`（必需）: `text` 或 `url`
- `sourceContent`（必需）: 文本或 URL
- `speakerId`（必需）: 音色 ID
- `language`（可选）: `zh` 或 `en`
- `mode`（可选，默认 smart）: `smart`（AI 增强）或 `direct`（原文）

## CreateVideo 工作流中的用法

1. 先调用 `get_speakers` 获取你的主播音色 ID（或使用平台提供的公共音色）
2. 调用 `create_podcast` 生成双人播客：
   - `query`: 用户提供的文案
   - `speakerIds`: [YOUR_SPEAKER_ID_1, YOUR_SPEAKER_ID_2]
   - `language`: "zh"
   - `mode`: "quick"
3. 播客生成完成后，下载音频文件到任务目录
