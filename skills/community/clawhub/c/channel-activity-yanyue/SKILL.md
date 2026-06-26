---
name: channel-activity
description: Multi-channel short-term memory for AI assistants
version: 3.0.0
tags: memory, multi-channel, context, summary
---

# Channel Activity

Record and query activities from different channels with 30-minute TTL.

## Install

```bash
npx clawhub@latest install channel-activity
```

## Usage

```python
from channel_activity import ChannelActivity

ca = ChannelActivity()
ca.record("feishu", "Task request")
summary = ca.get_context_summary(channel="qq")
```

## Features

- Multi-channel support (Feishu, QQ, etc.)
- 30-minute TTL with auto cleanup
- Smart summarization (50 chars/message)
- Cross-channel query

## License

MIT
