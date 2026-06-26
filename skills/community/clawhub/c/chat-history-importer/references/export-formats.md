# Supported Export Formats

This skill supports OpenAI ChatGPT and Anthropic Claude conversation exports.

## OpenAI ChatGPT Export

1. Go to **Settings → Data Controls → Export data**
2. Download your data as ZIP
3. Extract `conversations.json`

**Format:**

```json
[
  {
    "id": "chat_abc123...",
    "title": "Some topic",
    "create_time": 1712345678.123,
    "messages": [
      {
        "role": "user" | "assistant" | "system",
        "content": { "parts": [ "text..." ] } | "text...",
        "create_time": 1712345678.123
      }
    ]
  }
]
```

## Anthropic Claude Export

1. Go to **Settings → Privacy → Export data**
2. Download your data as ZIP
3. Extract `conversations.json`

**Format:**

```json
[
  {
    "uuid": "conv_abc123...",
    "name": "Conversation title",
    "created_at": "2025-01-15T10:30:00Z",
    "chat_messages": [
      {
        "sender": "human" | "assistant",
        "text": "message content",
        "created_at": "2025-01-15T10:30:00Z"
      }
    ]
  }
]
```

## Auto-Detection

The skill auto-detects format by inspecting the JSON structure. You can also specify `--format openai` or `--format anthropic` explicitly.

## Processing

Both formats are normalized to:

```json
{
  "id": "source_uuid",
  "title": "chat title",
  "date": "YYYY-MM-DD",
  "messages": [
    {
      "role": "user" | "assistant",
      "content": "text",
      "timestamp": "ISO8601"
    }
  ]
}
```
