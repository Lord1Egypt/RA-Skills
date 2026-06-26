# AstrBot Advanced Features

## Plugin Configuration With `_conf_schema.json`

When a plugin needs user configuration, add `_conf_schema.json` in the plugin root.

### Schema Fields

- `type`: supports `string`, `text`, `int`, `float`, `bool`, `object`, `list`, `dict`, `file`, and `template_list`.
- `description`: short explanation of the config item.
- `hint`: tooltip text.
- `obvious_hint`: whether the hint should be emphasized.
- `default`: default value.
- `items`: sub-schema for `object`.
- `invisible`: hide from WebUI.
- `options`: dropdown options.
- `editor_mode`, `editor_language`, `editor_theme`: code-editor options.
- `_special`: values such as `select_provider`, `select_provider_tts`, `select_provider_stt`, and `select_persona`.

### Basic Example

```json
{
  "api_key": {
    "description": "API Key",
    "type": "string",
    "hint": "第三方服务密钥",
    "default": ""
  },
  "mode": {
    "description": "Operation Mode",
    "type": "string",
    "options": ["chat", "agent", "workflow"]
  },
  "llm_provider": {
    "description": "选择模型提供商",
    "type": "string",
    "_special": "select_provider"
  }
}
```

### Accessing Config

```python
from astrbot.api import AstrBotConfig


class ConfigPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
```

## Session Control

Use `session_waiter` for multi-turn interactions:

```python
from astrbot.core.utils.session_waiter import SessionController, session_waiter


@filter.command("ask-name")
async def ask_name(self, event: AstrMessageEvent):
    """询问用户名。"""
    yield event.plain_result("你叫什么名字？")

    @session_waiter(timeout=30)
    async def waiter(controller: SessionController, event: AstrMessageEvent):
        await event.send(event.plain_result(f"你好，{event.message_str}！"))
        controller.stop()

    await waiter(event)
```

Session flows can also use `controller.keep(...)`, `controller.stop()`, history chains, or a custom `SessionFilter` for group-wide sessions.

## AI / LLM Integration

### Calling LLM Directly

```python
@filter.command("ask")
async def ask(self, event: AstrMessageEvent, question: str):
    umo = event.unified_msg_origin
    provider_id = await self.context.get_current_chat_provider_id(umo=umo)
    llm_resp = await self.context.llm_generate(
        chat_provider_id=provider_id,
        prompt=question,
    )
    yield event.plain_result(llm_resp.completion_text)
```

### Calling LLM Via Provider

```python
@filter.command("chat")
async def chat(self, event: AstrMessageEvent):
    provider = self.context.get_using_provider(umo=event.unified_msg_origin)
    if provider:
        llm_resp = await provider.text_chat(prompt="Hi!")
        yield event.plain_result(llm_resp.completion_text)
```

Other provider types are also available through context, including STT, TTS, and embedding providers.

## LLM Hooks

Follow these exact signatures when using request/response hooks:

```python
from astrbot.api.provider import LLMResponse, ProviderRequest


@filter.on_llm_request()
async def on_llm_request(self, event: AstrMessageEvent, req: ProviderRequest):
    req.system_prompt += "\n请保持简洁。"


@filter.on_llm_response()
async def on_llm_response(self, event: AstrMessageEvent, resp: LLMResponse):
    print(resp)
```

Hook restrictions:

- These hook methods must be `async def`.
- `on_llm_request` and `on_llm_response` must each have three parameters.
- In `on_llm_request`, `on_llm_response`, `on_decorating_result`, and `after_message_sent`, do not use `yield`. Use `await event.send(...)` if you need to send a message.

## LLM Tools

Preferred approach: register tool objects in `__init__`.

```python
from dataclasses import dataclass, field

from astrbot.api import FunctionTool


@dataclass
class GetWeatherTool(FunctionTool):
    name: str = "get_weather"
    description: str = "获取指定地点的天气。"
    parameters: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名"}
            },
            "required": ["location"],
        }
    )

    async def run(self, event: AstrMessageEvent, location: str):
        return f"{location} 晴"


class ToolPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.context.add_llm_tools(GetWeatherTool())
```

Decorator form is also available:

```python
@filter.llm_tool(name="get_weather")
async def get_weather(self, event: AstrMessageEvent, location: str):
    """获取天气。

    Args:
        location(string): 地点
    """
    return f"{location} 晴"
```

Important reviewer-facing rule:

- Do not combine `@filter.permission_type(...)` with `@filter.llm_tool(...)` on the same method.

## Agents

### Tool-Loop Agent

```python
@filter.command("agent")
async def agent_cmd(self, event: AstrMessageEvent, query: str):
    umo = event.unified_msg_origin
    prov_id = await self.context.get_current_chat_provider_id(umo)
    llm_resp = await self.context.tool_loop_agent(
        event=event,
        chat_provider_id=prov_id,
        prompt=query,
        max_steps=30,
    )
    yield event.plain_result(llm_resp.completion_text)
```

### Multi-Agent

You can build sub-agents as tools that internally call `self.context.tool_loop_agent(...)`, then compose them inside a parent agent flow.

## Conversation And Persona Managers

Useful context services:

- `self.context.conversation_manager`
- `self.context.persona_manager`

Use them when a plugin needs direct access to conversation history or persona selection.

## Text To Image

### Basic

```python
@filter.command("image")
async def image(self, event: AstrMessageEvent, text: str):
    """把文字转成图片。"""
    url = await self.text_to_image(text)
    yield event.image_result(url)
```

### Custom HTML + Jinja2

```python
template = """
<div style="font-size: 32px;">
  <h1>Todo List</h1>
  <ul>
  {% for item in items %}
    <li>{{ item }}</li>
  {% endfor %}
  </ul>
</div>
"""

url = await self.html_render(template, {"items": ["Item 1", "Item 2"]})
```
