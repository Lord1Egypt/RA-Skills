# Integration Notes

## Primary endpoint

- Web chat: `https://whylingxi.cn/chat`

## Request pattern

First turn:

```json
{
  "message": "我30岁，想买保险"
}
```

Later turns:

```json
{
  "session_id": "abc-123",
  "message": "预算5000，帮我规划方案"
}
```

The remote service returns a `session_id` and uses it to load prior conversation on the server side.

## Local multi-turn handling

The local script stores a mapping from local `--session-id` to upstream `session_id` at:

`~/.openclaw/workspace-xiaoma/.skill-sessions/china-insurance-advisor/session_map.json`

Use `--reset-session` to clear the stored mapping for a fresh conversation.

## Notes

- This skill is a thin proxy, not a local insurance planner
- Do not add local product logic unless the user explicitly asks for summarization or analysis of the returned answer
- If the endpoint behavior changes, update the script to match the remote chat contract
