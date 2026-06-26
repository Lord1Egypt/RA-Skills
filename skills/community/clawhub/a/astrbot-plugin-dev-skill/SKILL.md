---
name: astrbot-plugin-dev
description: Guide for developing AstrBot plugins that match the AstrBot main repo, pass astr-plugin-reviewer checks, and cover commands, filters, hooks, LLM integrations, and agents. Use when requested to create or update an AstrBot plugin.
---

# AstrBot Plugin Development

Use this skill to write AstrBot plugins in a reviewer-first way: align with `astr-plugin-reviewer` hard checks, then follow the current AstrBot repository APIs and docs.

## Start Here

Before writing code, always read these two references first:

- [references/reviewer-checklist.md](references/reviewer-checklist.md): hard constraints from `astr-plugin-reviewer` and plugin-market submission checks.
- [references/project-structure.md](references/project-structure.md): required files, metadata rules, local dev flow, and publishing expectations.

Then load only the references you need:

- [references/core-api.md](references/core-api.md): imports, decorators, handler signatures, hook constraints, platform compatibility.
- [references/advanced-features.md](references/advanced-features.md): config schema, session control, LLM tools, direct LLM calls, agents, and T2I.
- [references/message-components.md](references/message-components.md): message-chain composition, passive replies, and proactive messages.
- [references/patterns.md](references/patterns.md): reviewer-friendly implementation patterns, persistence, async networking, and platform access.

## Default Workflow

1. Create or verify `main.py` and `metadata.yaml` first.
2. Treat `metadata.yaml` as the source of truth for plugin identity. Prefer `desc` plus `repo`, and never keep both `desc` and `description`.
3. In `main.py`, define a class that inherits `Star`. Prefer AstrBot's auto-discovery; do not introduce the deprecated `@register` decorator unless you are maintaining old code.
4. Import `filter` exactly with `from astrbot.api.event import filter` to avoid reviewer failures and naming confusion.
5. Import the logger exactly with `from astrbot.api import logger`.
6. Keep network I/O async. Prefer `httpx` or `aiohttp`; do not use `requests`, blocking sleeps, or other blocking network calls.
7. If the plugin needs persistent files, prefer `StarTools.get_data_dir()`. It returns a `Path`.
8. If you implement LLM hooks, LLM tools, direct LLM calls, or agents, follow the exact signatures and restrictions in [references/advanced-features.md](references/advanced-features.md).
9. Before finishing, run a self-check against [references/reviewer-checklist.md](references/reviewer-checklist.md). If the user wants marketplace publishing, also ensure the publish JSON matches `metadata.yaml` exactly.

## Minimal Template

```python
from pathlib import Path

from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star, StarTools


class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.data_dir: Path = StarTools.get_data_dir()

    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """回复一个简单问候。"""
        logger.info(f"helloworld triggered by {event.get_sender_id()}")
        yield event.plain_result(f"Hello, {event.get_sender_name()}!")

    async def terminate(self):
        """Called when the plugin is unloaded or disabled."""
```

**Note**: The `@register` decorator is deprecated in newer versions of AstrBot. Please use `metadata.yaml` to define plugin metadata. AstrBot automatically detects the plugin class inheriting from `Star`.

## Core Workflows

### 1. Project Setup and Metadata

A complete plugin requires `metadata.yaml` for identification, `requirements.txt` for dependencies, and optionally `logo.png`, `_conf_schema.json`, and a `README.md`.

- Plugin names should start with `astrbot_plugin_`, be lowercase, have no spaces, and be short.
- See [references/project-structure.md](references/project-structure.md) for mandatory files, dev environment setup, and publishing.

### 2. Registering Commands and Filters

Commands are registered using `@filter.command(name)`. AstrBot auto-parses command parameters by type hints. You can also use command groups, command aliases, and filter by event type, platform, or user permission.

- See [references/core-api.md](references/core-api.md) for full list of filters, hooks, the platform compatibility matrix, and event propagation control.

### 3. Handling Messages and Responses

AstrBot uses a message-chain system. You can respond with plain text, images, or a mix of components. Proactive messages are supported via `unified_msg_origin` and `MessageChain`.

- See [references/message-components.md](references/message-components.md) for how to build and send messages.

### 4. Advanced Integrations

- **Configuration**: Use `_conf_schema.json` for user settings.
- **LLM Tools**: Register tools via `@filter.llm_tool` or `FunctionTool`.
- **LLM Direct Calls**: Use `self.context.llm_generate()` to call LLMs directly.
- **Agent / Multi-Agent**: Use `self.context.tool_loop_agent()` for tool-loop agents.
- **Stateful Interaction**: Use `session_waiter` for multi-step prompts with custom session filters.
- **T2I**: Render text or HTML/Jinja2 templates to images.
- **Conversation & Persona Managers**: Access LLM conversation history and persona settings when needed.

See [references/advanced-features.md](references/advanced-features.md) for examples.

## Elegant Design Patterns

Follow these patterns for robust, user-friendly plugins:

- Use unified logging via `from astrbot.api import logger`.
- Handle errors gracefully to avoid bot crashes.
- Use KV storage or the plugin data directory for persistence.
- Ensure all I/O operations are non-blocking.
- Access platform instances, loaded plugins, and protocol-level APIs only when necessary.

See [references/patterns.md](references/patterns.md) for detailed code patterns.
