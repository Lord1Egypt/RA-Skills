# Config Schema

Use a JSON file like this:

```json
{
  "provider": "OpenAI-Compatible",
  "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
  "api_key": "YOUR_KEY",
  "model_id": "ark-code-latest"
}
```

You can generate this file automatically:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" init-config \
  --provider "OpenAI-Compatible" \
  --base-url "https://api.siliconflow.cn/v1/chat/completions" \
  --api-key "$API_KEY" \
  --model-id "deepseek-ai/DeepSeek-V3.2" \
  --config-output ./provider.json
```

For batch use, normalize a raw list into `providers.json`:

```bash
python "$CODEX_HOME/skills/api-quality-check/scripts/api_quality_check.py" init-batch-config \
  --configs ./raw-providers.json \
  --config-output ./providers.json
```

Optional field:

```json
{
  "headers": {
    "X-Client-Name": "example-client"
  },
  "extra_body": {
    "thinking": {
      "type": "disabled"
    }
  }
}
```

Notes:

- `headers` must be a JSON object. Values are sent as request headers and can override defaults such as `User-Agent`.
- Use vendor-specific headers only when that vendor requires them. For Kimi coding, `{"User-Agent":"KimiCLI/2.0.0"}` is only for `https://api.kimi.com/coding` endpoints; for the OpenAI-compatible Kimi endpoint, use `https://api.kimi.com/coding/v1`.
- If `extra_body` is omitted, the script auto-adds `{"thinking":{"type":"disabled"}}` for common reasoning-first providers such as Ark/Doubao/GLM/Zhipu.
- `provider` may be `OpenAI`, `OpenAI-Compatible`, or `Anthropic`.
- `base_url` should preferably be the API root, but for OpenAI/OpenAI-compatible configs the script also accepts a full `/chat/completions` URL and normalizes it automatically.
- `init-config` writes the normalized `base_url` and any auto-selected `extra_body` explicitly into the saved config.
- `init-batch-config` applies the same normalization to every item in a config list and emits a top-level `{"configs":[...]}` object.
- Anthropic mode is treated as B3IT-only in this skill.

## Batch config schema

Use either a top-level array:

```json
[
  {
    "name": "ark-prod",
    "provider": "OpenAI-Compatible",
    "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
    "api_key": "YOUR_KEY",
    "model_id": "ark-code-latest"
  },
  {
    "name": "glm-prod",
    "provider": "OpenAI-Compatible",
    "base_url": "https://open.bigmodel.cn/api/coding/paas/v4",
    "api_key": "YOUR_KEY",
    "model_id": "glm-4.7"
  }
]
```

Or an object with `configs`:

```json
{
  "configs": [
    {
      "name": "ark-prod",
      "provider": "OpenAI-Compatible",
      "base_url": "https://ark.cn-beijing.volces.com/api/coding/v3",
      "api_key": "YOUR_KEY",
      "model_id": "ark-code-latest"
    }
  ]
}
```

Notes:

- `name` is optional but recommended; it is used in batch output labels.
- Each item follows the same schema as a single-provider config.
- A ready-to-edit example file is available at `references/providers.example.json`.
