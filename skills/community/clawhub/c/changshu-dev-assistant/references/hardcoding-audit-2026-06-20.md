# Hardcoding Audit & Fix — 2026-06-20

## Audit Findings

### changshu_assistant_main.py
| Line (pre-fix) | Hardcoded Value | Fix |
|---|---|---|
| `LLMClient.__init__` | `model_name='gpt-3.5-turbo'`, `provider='openai'` | New `_resolve()` method: env var → config.yaml → empty string |
| `_call_openai` | `api_base or "https://api.openai.com/v1"` | Empty-check with error message, no fallback URL |
| `_call_anthropic` | `api_base or "https://api.anthropic.com/v1"` | Same pattern |
| `call_llm` | `if self.provider == 'openai'` routing | Default route is openai-compatible for any non-anthropocustom provider |

### config.yaml
| Issue | Fix |
|---|---|
| `api_key: "nvapi-vo7u..."` NVIDIA key in plaintext | Set to `""`, comment points to `LLM_API_KEY` env var |
| `model: "openai"` (duplicate with provider) | Removed |
| `ai_provider: "openai"` in preferences | Set to `""` |
| `provider: "openai"` with misleading comment | Set to `""`, comment updated |
| `model_name: "minimaxai/minimax-m2.7"` with wrong "Llama" comment | Set to `""` |

### model_selection.json (DELETED)
- Contained only gemma-7b-it, mistral-7b, llama2-70b, yi-34b — all outdated
- Zero code references (confirmed via grep)
- No replacement needed; model selection is now dynamic via env vars

### Documentation files cleaned
- RUNNING_MODE.md, LLM_INTEGRATION_COMPLETE.md, SIMPLE_GUIDE.md, LLM_CONFIG_GUIDE.md (full rewrite), LLM_UPDATE.md, NVIDIA_CONFIG_SUCCESS.md, templates/QUICKSTART.md

## Environment Variable Scheme

```bash
LLM_PROVIDER    # openai-compat( default) | anthropic | custom
LLM_API_KEY     # never in config files
LLM_API_BASE    # full URL without /chat/completions suffix
LLM_MODEL_NAME  # any model the provider supports
```

Priority: env var > config.yaml > empty (triggers error message, not silent fallback)

## _resolve() Pattern (reusable)

```python
ENV_MAP = {
    'provider': 'LLM_PROVIDER',
    'api_key': 'LLM_API_KEY',
    'api_base': 'LLM_API_BASE',
    'model_name': 'LLM_MODEL_NAME',
}

def _resolve(self, key):
    env_val = os.environ.get(self.ENV_MAP.get(key, ''), '')
    if env_val:
        return env_val
    return self.config.get(key, '')
```

## Scan Regex (reuse for future audits)

```
nvapi-|sk-[a-zA-Z0-9]{20,}|gpt-3\.5-turbo|api\.openai\.com|api\.anthropic\.com|你的API密钥
```
