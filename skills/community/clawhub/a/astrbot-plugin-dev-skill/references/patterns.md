# AstrBot Reviewer-Friendly Patterns

These patterns are chosen to satisfy both AstrBot's runtime model and `astr-plugin-reviewer`.

## Logging

Use AstrBot's logger only:

```python
from astrbot.api import logger

logger.info("plugin initialized")
logger.error(f"request failed: {exc}")
```

Avoid:

- `import logging`
- `logging.getLogger(...)`
- third-party loggers such as `loguru`

## Persistence

Prefer `StarTools.get_data_dir()` for plugin-owned runtime files:

```python
from pathlib import Path

from astrbot.api.star import StarTools

data_dir: Path = StarTools.get_data_dir()
cache_file = data_dir / "cache.json"
```

Notes:

- `get_data_dir()` returns a `Path`, not a string.
- Keep runtime data out of the plugin source directory.
- Bundled assets can stay in the repo; mutable runtime data should not.

### KV Storage

In newer AstrBot versions you can also use simple per-plugin KV helpers:

```python
await self.put_kv_data("key", value)
value = await self.get_kv_data("key", default)
await self.delete_kv_data("key")
```

## Async Network Access

Use async HTTP clients:

```python
import httpx


async with httpx.AsyncClient(timeout=10) as client:
    resp = await client.get(url)
    resp.raise_for_status()
```

Avoid:

- `requests`
- blocking polling loops
- `time.sleep(...)` in async flows

## Error Handling

Wrap external calls and user-driven parsing so one failure does not crash the plugin:

```python
try:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url)
        resp.raise_for_status()
except Exception as exc:
    logger.error(f"fetch failed: {exc}")
    yield event.plain_result("请求失败，请稍后再试。")
```

## Handler Documentation

- Give command handlers a short docstring. AstrBot can surface it in help output.
- Keep handler logic thin and move business logic into helper modules when complexity grows.

## Hook Messaging Rules

For these hooks, send messages with `await event.send(...)`, never `yield`:

- `@filter.on_llm_request()`
- `@filter.on_llm_response()`
- `@filter.on_decorating_result()`
- `@filter.after_message_sent()`

## Accessing Platform Instances

```python
platform = self.context.get_platform(filter.PlatformAdapterType.AIOCQHTTP)
```

If you need protocol-specific behavior, guard it by platform type before calling adapter-specific APIs.

## Querying Loaded Plugins And Platforms

```python
plugins = self.context.get_all_stars()
platforms = self.context.platform_manager.get_insts()
```

## Delivery Checklist

- Code targets Python 3.10.
- Network I/O is async.
- Logging uses `from astrbot.api import logger`.
- Persistent data uses `StarTools.get_data_dir()` when applicable.
- User-facing failures are handled gracefully.
- Run `ruff format` and any relevant tests before delivery.
- Test the plugin before publishing.
