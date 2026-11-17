# CLI / API Fallback 政策

上游 `codex-ppt-skill` 支援 API/CLI fallback；本 fork 預設關閉。

禁止自動讀取或要求：

- `OPENAI_API_KEY`
- 第三方 image API key
- OpenAI-compatible relay key

禁止因為：

- 想要更高解析度
- built-in image generation 暫時不可用
- 想指定 output path

就自動切換 API 計費模式。

只有使用者明確要求改變 backend policy 時，AGY 才能建立新的 backend decision；若這需要修改程式或 routing，交給明確指派的 Codex Production Engineering Worker 或 Kiro。
