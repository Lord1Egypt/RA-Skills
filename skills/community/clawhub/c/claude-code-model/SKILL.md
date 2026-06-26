---
name: claude-code-model
description: Configure Claude Code to use custom models (DeepSeek, GLM, Qwen, etc.). Use when user wants to change Claude Code's model, switch API provider, or set up custom model endpoints. Triggers on phrases like "change claude model", "switch claude to deepseek", "configure claude code model", "claude用别的模型".
---

# Claude Code Model Configuration

Switch Claude Code to use custom model providers (DeepSeek, GLM, Qwen, OpenAI-compatible endpoints).

## Configuration Locations

Claude Code reads config from multiple sources (in priority order):

1. **Environment variables** (highest priority)
2. **`~/.claude/config.json`**
3. **`~/.claude/settings.json`**

## Required Parameters

User must provide:
- **base_url**: API endpoint (e.g., `https://api.deepseek.com/anthropic`)
- **model**: Model name (e.g., `deepseek-v4-flash`, `glm-5`)
- **api_key**: API key

## Workflow

### Step 1: Update Environment Variables

Set user-level environment variables (persist across restarts):

```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "<api_key>", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "<base_url>", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_MODEL", "<model>", "User")
```

Clear conflicting variables:

```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "", "User")
```

### Step 2: Update config.json

Edit `~/.claude/config.json`:

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "<api_key>",
    "ANTHROPIC_BASE_URL": "<base_url>",
    "ANTHROPIC_MODEL": "<model>"
  }
}
```

### Step 3: Update settings.json

Edit `~/.claude/settings.json`, add/update:

```json
{
  "model": "<model>",
  "env": {
    "ANTHROPIC_BASE_URL": "<base_url>",
    "ANTHROPIC_API_KEY": "<api_key>"
  }
}
```

### Step 4: Verify

Test the configuration:

```bash
claude --print "hi, what model are you?"
```

## Common Issues

- **Auth conflict**: Both `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` set → Clear `ANTHROPIC_AUTH_TOKEN`
- **Old model still shows**: Check `config.json` for stale `ANTHROPIC_MODEL` value
- **Changes not生效**: New terminal window required for env var changes

## Popular Provider Examples

| Provider | base_url | Models |
|----------|----------|--------|
| DeepSeek | `https://api.deepseek.com/anthropic` | `deepseek-v4-flash`, `deepseek-v4-pro` |
| GLM (阿里云) | `https://coding.dashscope.aliyuncs.com/apps/anthropic` | `glm-5` |
| Qwen | Same as GLM | `qwen-*` |

## Script

Use the bundled script for automated configuration:

```bash
python scripts/configure_model.py --base-url <url> --model <name> --api-key <key>
```