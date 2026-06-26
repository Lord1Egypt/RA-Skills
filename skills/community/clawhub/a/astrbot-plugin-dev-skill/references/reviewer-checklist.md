# `astr-plugin-reviewer` Checklist

Use this checklist before you consider an AstrBot plugin "done".

## Hard Rules From The Reviewer

### Runtime Assumptions

- Target Python 3.10.
- Assume an async runtime.
- Review and implementation should focus on non-blocking network I/O.

### `main.py` Structure

- `main.py` must contain a class inheriting from `Star`.
- Import `filter` with `from astrbot.api.event import filter`.
- Except for `@filter.on_astrbot_loaded()`, every `@filter` handler should accept `event: AstrMessageEvent`.
- `on_llm_request` and `on_llm_response` must each accept three parameters: `self`, `event`, and the request/response object.

### Logging

- Import logger with `from astrbot.api import logger`.
- Do not use `logging`, `logging.getLogger`, `loguru`, or other logging libraries.

### Async And Blocking Calls

- Do not use blocking network clients such as `requests`.
- Prefer `httpx.AsyncClient` or `aiohttp`.

### Persistence

- If the plugin stores runtime data, prefer `StarTools.get_data_dir()`.
- `StarTools.get_data_dir()` returns a `Path`.
- The intended data root is `data/plugin_data/<plugin_name>/`.

### Hook Restrictions

These hooks cannot use `yield` to send messages:

- `@filter.on_llm_request()`
- `@filter.on_llm_response()`
- `@filter.on_decorating_result()`
- `@filter.after_message_sent()`

Use `await event.send(...)` there instead.

### LLM Tool Restriction

- Do not combine `@filter.permission_type(...)` with `@filter.llm_tool(...)` on the same method.

## Metadata And Marketplace Consistency

The reviewer validates `metadata.yaml` before AI review.

Required consistency checks:

- `metadata.yaml` must exist.
- `metadata.yaml.name` must equal the submitted plugin name.
- `metadata.yaml.author` must equal the submitted author.
- `metadata.yaml.version` must exist.
- `metadata.yaml.repo` must equal the submitted repo URL.
- `metadata.yaml` must contain exactly one of `desc` or `description`.
- That `desc` or `description` value must equal the submitted JSON `desc`.

Recommended metadata template:

```yaml
name: astrbot_plugin_example
author: YourName
version: 1.0.0
desc: 一个示例插件
repo: https://github.com/yourname/astrbot_plugin_example
```

## Plugin-Market Submission Checks

If the user wants to publish to the AstrBot marketplace, validate these too:

- Issue title should be `[Plugin] 插件名`.
- The repository should be hosted on `github.com`.
- The issue body should include checked declarations matching these statements:
  - `我的插件经过完整的测试`
  - `我的插件不包含恶意代码`
  - `我已阅读并同意遵守该项目的 [行为准则](https://docs.github.com/zh/site-policy/github-terms/github-community-code-of-conduct)。`
- The issue body should include a ` ```json ` block with:

```json
{
  "name": "astrbot_plugin_example",
  "desc": "一个示例插件",
  "author": "YourName",
  "repo": "https://github.com/yourname/astrbot_plugin_example"
}
```

Keep this JSON aligned with `metadata.yaml`.

## Final Self-Check

- `main.py` contains a valid `Star` subclass.
- `metadata.yaml` is complete and internally consistent.
- Logging import is correct.
- No blocking network I/O.
- Persistent data path is reviewer-friendly.
- Hook signatures and hook send semantics are correct.
- Command handlers have short docstrings.
- Code has been tested and formatted with `ruff`.
