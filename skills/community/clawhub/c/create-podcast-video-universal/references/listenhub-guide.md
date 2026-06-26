# ListenHub MCP 参考

## 安装

```bash
npx -y @marswave/listenhub-mcp-server
```

## 工具列表

### get_speakers
查询可用音色。
- 参数：`language`（可选，默认 zh）

### create_flowspeech
文本转语音。
- 参数：
  - `sourceType`: "text"
  - `sourceContent`: 文案内容
  - `speakerId`: 音色ID（调用 get_speakers 获取）
  - `language`: "zh"
  - `mode`: "smart"（AI增强）或 "direct"（原文）

## 音色选择

首次使用建议：
1. 调用 `get_speakers(language="zh")`
2. 试听各音色，选定后使用其 ID
3. 建议记录选定的音色 ID，方便后续使用
