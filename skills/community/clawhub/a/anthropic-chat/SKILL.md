# anthropic-chat — Anthropic Messages API 调用

## 功能
直接通过 Anthropic Messages API 与 Claude 对话。

## 环境变量
- `ANTHROPIC_API_KEY` — Anthropic API key（必填）

## 调用方式
- `sessions_spawn` + `runtime=acp`，在 `task` 里写自然语言描述任务
- Skill 会自动使用 Messages API 发送请求并返回结果

## 认证
直接使用用户已有的 API key，不需要额外认证。

## 示例任务
- "让 anthropic-chat 用 Claude Opus 4 解释量子纠缠"
- "调用 anthropic-chat，用 Sonnet 4 写一首关于月亮的诗"
