# AstrBot Core API Reference

## Canonical Imports

Use these imports unless the current plugin already follows another valid AstrBot pattern:

```python
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, StarTools
```

Notes:

- `filter` should be imported from `astrbot.api.event`, not shadowed by Python's built-in `filter`.
- `logger` should come from `astrbot.api`, not `logging` or third-party logger packages.
- `register` still exists in `astrbot.api.star`, but it is deprecated. Prefer a plain `Star` subclass plus `metadata.yaml`.

## Core Objects

### `Star`

- Base class for plugins.
- Handlers should be methods on the `Star` subclass.
- `context: Context` is the runtime context object.
- `config` may be passed into `__init__` when `_conf_schema.json` exists.
- `terminate()` is optional and runs when the plugin is unloaded.
- `text_to_image(...)` and `html_render(...)` are available for image rendering.
- KV helpers such as `put_kv_data`, `get_kv_data`, and `delete_kv_data` are available in newer versions.

### `Context`

- AstrBot runtime context for plugin services and registration.
- `send_message(umo, chains)`: send a proactive message to a session.
- `get_using_provider(umo)`: get the current LLM provider.
- `get_provider_by_id(provider_id)`: get a specific provider.
- `get_current_chat_provider_id(umo)`: get the active chat model provider ID.
- `llm_generate(...)`: call an LLM directly.
- `tool_loop_agent(...)`: run a tool-loop agent.
- `get_platform(adapter_type)`: get a platform adapter instance.
- `add_llm_tools(*tools)`: register LLM tools.
- `get_all_stars()`: get loaded plugins.
- `conversation_manager` and `persona_manager`: access conversation and persona services.

### `StarTools`

- Use `StarTools.get_data_dir()` for persistent plugin data.
- It returns a `Path` pointing at `data/plugin_data/<plugin_name>/`.

### `AstrMessageEvent`

- `message_str`: plain-text message.
- `message_obj`: structured message object.
- `unified_msg_origin`: session identifier for proactive messages and provider selection.
- `get_sender_id()`, `get_sender_name()`, `get_group_id()`, `get_platform_name()`: sender and platform helpers.
- `plain_result(text)`, `image_result(path_or_url)`, `chain_result(chain)`, `make_result()`: build results.
- `send(result)`: send directly when a hook cannot use `yield`.
- `get_result()`: inspect or modify the current result in decorating hooks.
- `stop_event()`: stop later processing.

### `AstrBotMessage`

Available through `event.message_obj` and contains the parsed message chain plus the raw platform payload.

## Commands And Decorators

- `@filter.command(name, alias=set(), priority=0)`
- `@filter.command_group(name, alias=set())`
- `@filter.regex(pattern)`
- `@filter.event_message_type(type)`
- `@filter.permission_type(type)`
- `@filter.platform_adapter_type(type)`
- `@filter.on_astrbot_loaded()`
- `@filter.on_waiting_llm_request()`
- `@filter.on_llm_request()`
- `@filter.on_llm_response()`
- `@filter.on_decorating_result()`
- `@filter.after_message_sent()`
- `@filter.llm_tool(name="...")`

## Command Parameters

`@register` is deprecated in newer versions. Please use `metadata.yaml` to define plugin metadata. AstrBot will automatically detect the plugin class inheriting from `Star`.

AstrBot can auto-parse command parameters from type hints:

```python
@filter.command("add")
async def add(self, event: AstrMessageEvent, a: int, b: int):
    yield event.plain_result(f"Result: {a + b}")
```

## Command Groups

```python
@filter.command_group("math")
def math(self):
    pass


@math.command("add")
async def add(self, event: AstrMessageEvent, a: int, b: int):
    yield event.plain_result(f"Result: {a + b}")
```

## Event Filters

You can combine filters to constrain handlers by event type, platform, permission, or regex.

```python
@filter.command("secret")
@filter.permission_type(filter.PermissionType.ADMIN)
@filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
async def secret_cmd(self, event: AstrMessageEvent):
    yield event.plain_result("Admin-only private command!")
```

## Hooks

Event hooks should not be mixed casually with normal command semantics.

- `@filter.on_astrbot_loaded()`: runs after AstrBot initialization.
- `@filter.on_waiting_llm_request()`: runs before acquiring the session lock; useful for "thinking..." messages.
- `@filter.on_llm_request()`: receives `(self, event, req: ProviderRequest)`.
- `@filter.on_llm_response()`: receives `(self, event, resp: LLMResponse)`.
- `@filter.on_decorating_result()`: modify `event.get_result().chain` before sending.
- `@filter.after_message_sent()`: runs after a message is sent.

## Handler Rules That Matter To The Reviewer

- Except for `@filter.on_astrbot_loaded()`, every `@filter` handler should accept an `event: AstrMessageEvent` parameter.
- For normal commands and listeners, use `yield event.plain_result(...)` or other result builders.
- In `on_llm_request`, `on_llm_response`, `on_decorating_result`, and `after_message_sent`, do not use `yield`; call `await event.send(...)` if you need to send a message.
- `on_llm_request` and `on_llm_response` must each accept three parameters: `self`, `event`, and the request/response object.
- Do not combine `@filter.permission_type(...)` with `@filter.llm_tool(...)` on the same method; that permission control is not valid there.

## LLM Tools

`@filter.llm_tool(...)` registers a tool via decorator. Tool objects can also be registered through `self.context.add_llm_tools(...)`.

## Controlling Event Propagation

```python
@filter.command("check")
async def check(self, event: AstrMessageEvent):
    if not self.is_valid():
        yield event.plain_result("Check failed")
        event.stop_event()
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

If the target platform is known, keep your handlers and message components compatible with that adapter.
