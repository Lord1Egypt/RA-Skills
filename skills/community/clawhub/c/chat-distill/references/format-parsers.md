# Chat Format Parsers

## Goal

Convert raw chat exports into a normalized message list:

```
[
  { "speaker": "张三", "text": "哈哈哈好搞笑", "time": "2024-01-15 10:30" },
  { "speaker": "李四", "text": "真的吗", "time": "2024-01-15 10:31" },
  ...
]
```

## Format Detection

Inspect file content and extension:

| Signature | Format |
|---|---|
| Lines match `YYYY-MM-DD HH:MM 昵称(微信号): msg` or `昵称: msg` | WeChat plain-text export |
| Lines match `HH:MM 昵称\nmsg` (two-line) | WeChat two-line export |
| Lines match `昵称 HH:MM\nmsg` | Variant two-line |
| File is `.json` and contains array of `{sender, content, time}` | JSON chat log |
| Lines match `HH:MM - Name: msg` | WhatsApp-style export |
| Lines match `Name [time]: msg` | Telegram desktop export |
| Free-form `Name: msg` per line (no timestamp) | Simple text transcript |

If unsure, ask the user.

## WeChat Plain-Text

Pattern (Chinese locale):

```
2024-01-15 10:30:15 张三
消息内容（可能多行）

2024-01-15 10:31:02 李四
另一条消息
```

Also variant with content on same line:

```
2024-01-15 10:30 张三: 消息内容
```

Parsing rules:
- Split on lines matching `^\d{4}-\d{2}-\d{2} \d{2}:\d{2}`.
- Extract speaker name after timestamp.
- Everything until next timestamp line is message body.
- Skip system messages (contain "撤回了一条消息", "加入了群聊", etc.).

## JSON Format

Expect either:

```json
[{"sender":"张三","content":"hello","time":"2024-01-15T10:30:00"}]
```

or nested structures. Normalize keys to `speaker`, `text`, `time`.

## WhatsApp Export

```
15/01/2024, 10:30 - Alice: Hello!
15/01/2024, 10:31 - Bob: Hi there
```

## Telegram Export

```
Alice [15 Jan 2024 10:30:00]
Hello!

Bob [15 Jan 2024 10:31:00]
Hi there
```

## Simple Text Transcript

```
张三: 今天天气真好
李四: 是啊
张三: 要不要出去走走
```

## Notes

- Skip messages that are purely media references like `[图片]`, `[表情]`, `[语音]` unless analyzing emoji/media usage patterns.
- Trim whitespace from message text.
- Preserve original casing for analysis.
