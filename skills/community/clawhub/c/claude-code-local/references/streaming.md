# Stream-JSON Processing

## Event Types

stream-json 输出包含以下事件类型：

| type | Description |
|------|-------------|
| `system/init` | Session start, available tools and model |
| `system/status` | Status change (requesting, etc.) |
| `stream_event/content_block_start` | New content block |
| `stream_event/content_block_delta` | Incremental token/text |
| `stream_event/content_block_stop` | Content block complete |
| `stream_event/message_delta` | Token usage update |
| `stream_event/message_stop` | Message complete |
| `assistant` | Full assistant message |
| `result` | Final result with complete text |

## Event Fields

### content_block_delta

```json
{
  "type": "stream_event",
  "event": {
    "type": "content_block_delta",
    "index": 1,
    "delta": {
      "type": "text_delta",     // or "thinking_delta"
      "text": "..."              // incremental text
    }
  }
}
```

### result

```json
{
  "type": "result",
  "subtype": "success",
  "is_error": false,
  "result": "完整输出文本",
  "duration_ms": 12345,
  "num_turns": 1,
  "usage": { "input_tokens": 100, "output_tokens": 200 }
}
```

## Filtering Tips

### Extract text_delta only (with jq)
```bash
claude --bare -p "..." --output-format stream-json | \
  jq -rj 'select(.type=="stream_event" and .event.delta.type?=="text_delta") | .event.delta.text'
```

### Extract final result
```bash
claude --bare -p "..." --output-format stream-json | \
  jq -r 'select(.type=="result") | .result'
```

### Skip thinking
```bash
claude --bare -p "..." --output-format stream-json | \
  jq -c 'select(.type!="stream_event" or .event.delta.type!="thinking_delta")'
```

## When to Use Each Output Format

| Format | Use When |
|--------|----------|
| text (default) | Simple tasks, short outputs, human reading |
| json | Need to parse final result programmatically |
| stream-json | Long tasks, need incremental output, prevent timeout |
| stream-json + verbose | Need maximum observability during execution |
