# AstrBot Message Components

## Overview

A message in AstrBot is a `MessageChain`, which is a list-like sequence of message components. Import them via:

`import astrbot.api.message_components as Comp`

## Standard Components

### `Comp.Plain(text)`

Plain text message content.

In the aiocqhttp adapter, `Plain` text is auto-stripped of leading and trailing whitespace. Use zero-width space `\u200b` if you need to preserve spacing.

### `Comp.At(qq)`

At a specific user. Use `event.get_sender_id()` for the current sender.

### `Comp.Image.fromURL(url)`

Send an image from a URL. The URL should start with `http` or `https`.

### `Comp.Image.fromFileSystem(path)`

Send an image from the local file system.

### `Comp.Record(file, url)`

Send a voice message. `.wav` is the safest format.

### `Comp.Video.fromFileSystem(path)` / `Comp.Video.fromURL(url)`

Send a video message.

### `Comp.Reply(id)`

Reply to a specific message ID.

### `Comp.Face(id)`

Send a QQ emoji.

### `Comp.Node(uin, name, content)`

A node for group forwarded or merged messages, mainly on OneBot v11:

```python
node = Comp.Node(
    uin=123456,
    name="BotName",
    content=[Comp.Plain("hello"), Comp.Image.fromFileSystem("test.jpg")]
)
yield event.chain_result([node])
```

### `Comp.File(file, name)`

Send a file. Platform support varies.

## Creating A Chain

```python
chain = [
    Comp.At(qq=event.get_sender_id()),
    Comp.Plain("Hello, world!"),
    Comp.Image.fromURL("https://example.com/logo.png")
]
yield event.chain_result(chain)
```

Notes:

- Use `yield event.chain_result(chain)` in normal commands and listeners.
- In `on_llm_request`, `on_llm_response`, `on_decorating_result`, and `after_message_sent`, do not `yield`; use `await event.send(...)` instead.
- Platform support differs for some components such as reply, record, video, or merged forward messages. If the target platform is known, keep the chain compatible with that adapter.

## Proactive Messaging

Proactive messages are sent without a new triggering user message. Some platforms do not support them.

Use `event.unified_msg_origin` to capture the session identifier, persist it if needed, then send later via `self.context.send_message(...)`.

```python
from astrbot.api.event import MessageChain


@filter.command("subscribe")
async def subscribe(self, event: AstrMessageEvent):
    umo = event.unified_msg_origin
    self.subscriptions.append(umo)
    yield event.plain_result("Subscribed!")


async def notify_subscribers(self):
    for umo in self.subscriptions:
        message_chain = MessageChain().message("New update!")
        await self.context.send_message(umo, message_chain)
```

## Platform Compatibility Matrix

| Platform         | At  | Plain | Image | Record | Video | Reply | Proactive |
| ---------------- | --- | ----- | ----- | ------ | ----- | ----- | --------- |
| QQ (aiocqhttp)   | ✅  | ✅    | ✅    | ✅     | ✅    | ✅    | ✅        |
| Telegram         | ✅  | ✅    | ✅    | ✅     | ✅    | ✅    | ✅        |
| QQ Official      | ❌  | ✅    | ✅    | ❌     | ❌    | ❌    | ❌        |
| Lark             | ✅  | ✅    | ✅    | ❌     | ❌    | ✅    | ✅        |
| WeCom            | ❌  | ✅    | ✅    | ✅     | ❌    | ❌    | ❌        |
| DingTalk         | ❌  | ✅    | ✅    | ❌     | ❌    | ❌    | ❌        |
