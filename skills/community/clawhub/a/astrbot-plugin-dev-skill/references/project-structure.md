# AstrBot Plugin Project Structure

Write the plugin as AstrBot expects to load it, and as `astr-plugin-reviewer` expects to validate it.

## Plugin Naming Conventions

- Name should start with `astrbot_plugin_` when possible.
- No spaces.
- All lowercase.
- Keep it short and readable.

## Recommended Layout

```text
astrbot_plugin_example/
├── main.py                # Required. Plugin class must live here.
├── metadata.yaml          # Required. Reviewer and marketplace depend on it.
├── requirements.txt       # Optional. Third-party Python deps only.
├── _conf_schema.json      # Optional. WebUI configuration schema.
├── logo.png               # Optional. 1:1 plugin logo.
└── README.md              # Optional but recommended.
```

## `metadata.yaml`

Prefer this shape for new plugins:

```yaml
name: astrbot_plugin_example
display_name: Example Plugin
author: YourName
version: 1.0.0
desc: 一个示例插件
repo: https://github.com/yourname/astrbot_plugin_example
astrbot_version: ">=4.16,<5"
support_platforms:
  - aiocqhttp
  - telegram
```

Key rules:

- `name`, `author`, `version`, and `repo` are effectively mandatory for publishable plugins.
- Prefer `desc` for consistency with the plugin-market submission JSON.
- If you use `description` instead of `desc`, do not keep both fields at the same time.
- `repo` should be a valid GitHub repository URL when the plugin is intended for the marketplace.
- `astrbot_version` should use a normal PEP 440 version specifier, without a `v` prefix.
- `support_platforms` values should use AstrBot adapter keys such as `aiocqhttp`, `qq_official`, `telegram`, `wecom`, `lark`, `dingtalk`, `discord`, `slack`, `kook`, `vocechat`, `weixin_official_account`, `satori`, `misskey`, or `line`.

When the running AstrBot version does not satisfy `astrbot_version`, the plugin can be blocked from loading.

## `main.py`

- The plugin class file must be named `main.py`.
- Define at least one class inheriting from `Star`.
- Prefer AstrBot's auto-discovery over the deprecated `@register` decorator.
- Keep all handlers inside the plugin class. Services can live in other files, but handlers should call into them from `main.py`.

## `requirements.txt`

- List only third-party Python dependencies.
- Prefer async-compatible network libraries such as `httpx` or `aiohttp`.
- Do not introduce `requests` for network access.

## `_conf_schema.json`

- Use this only when the plugin needs user-configurable settings in WebUI.
- AstrBot will materialize and store config under `data/config/<plugin_name>_config.json`.
- Match the runtime access pattern shown in [advanced-features.md](advanced-features.md).

## Development Environment Setup

```bash
git clone https://github.com/AstrBotDevs/AstrBot
mkdir -p AstrBot/data/plugins
cd AstrBot/data/plugins
git clone <your-plugin-repo-url>
```

Open the `AstrBot` project in your editor, then work inside `data/plugins/<your_plugin>/`.

### Debugging

- AstrBot injects plugins at runtime.
- After modifying plugin code, use the AstrBot WebUI plugin management page to reload the plugin.
- If a plugin fails to load because of code errors, WebUI may offer a one-click reload fix flow depending on version.

## Publishing To The Plugin Market

1. Push the plugin repo to GitHub.
2. Visit [AstrBot Plugin Market](https://plugins.astrbot.app).
3. Click `+`, fill in the plugin info, and submit to GitHub.
4. Review the generated AstrBot issue and make sure its JSON matches `metadata.yaml`.

## Persistent Data

- Do not persist mutable data inside the plugin repository directory.
- Prefer `StarTools.get_data_dir()` and store runtime data under `data/plugin_data/<plugin_name>/`.
- Treat bundled static assets and runtime-generated data as separate concerns.

### Simple KV Storage

AstrBot also provides per-plugin KV helpers in newer versions:

```python
await self.put_kv_data("key", value)
value = await self.get_kv_data("key", default)
await self.delete_kv_data("key")
```
