# Access Modes

Use the same image payload for all direct Responses-compatible entries:

```json
{
  "model": "gpt-5.4",
  "input": "prompt or multimodal user content",
  "tools": [
    {
      "type": "image_generation",
      "model": "gpt-image-2",
      "size": "1024x1536",
      "quality": "high",
      "output_format": "png"
    }
  ],
  "tool_choice": { "type": "image_generation" },
  "stream": true
}
```

## official

Use when the user has an official OpenAI permission code/API key.

Accepted inputs:

- `--permission-code` or `--api-key`
- `OPENAI_API_KEY`
- Optional `--base-url` or `OPENAI_BASE_URL`, defaulting to `https://api.openai.com/v1`

Example:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode official \
  --permission-code "$OPENAI_API_KEY" \
  --prompt "一张白底产品海报，主体是一台透明外壳复古收音机" \
  --output output/radio.png
```

## proxy

Use when the user has a Responses-compatible proxy or aggregator.

Accepted inputs:

- `--base-url` or `GPT_IMAGE_BASE_URL`
- `--api-key` or `GPT_IMAGE_API_KEY`
- Optional `--provider-name`

The script accepts either a full `/responses` URL or a base URL such as `/v1`; it tries reasonable endpoint candidates.

Example:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode proxy \
  --base-url "$GPT_IMAGE_BASE_URL" \
  --api-key "$GPT_IMAGE_API_KEY" \
  --prompt "一套极简 App 图标，玻璃拟态，蓝绿配色" \
  --size 1024x1024 \
  --output output/app-icon.png
```

## reserved

Use when the user wants to consume the creator's reserved capacity through a relay service.

Accepted inputs:

- `--service-url` or `GPT_IMAGE_RELAY_URL`
- `--user-id` or `GPT_IMAGE_USER_ID`
- `--profile-name` or `GPT_IMAGE_PROFILE_NAME`
- `--purchase-key` or `GPT_IMAGE_PURCHASE_KEY`
- `--quota auto|free|credit|none`, default `auto`

Reserved mode calls:

1. `POST /api/session` to create/reuse a user.
2. `POST /api/session/register` if `--profile-name` is provided.
3. `POST /api/keys` with `validate` and `consume` if `--purchase-key` is provided.
4. `POST /api/keys` with `check_free`, `consume_free`, or `consume_credit` according to quota mode.
5. `POST /api/generate/jobs`, then polls `GET /api/generate/jobs/:id`.
6. Downloads `GET /api/generate/jobs/:id/image` after success.

Example:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode reserved \
  --service-url "$GPT_IMAGE_RELAY_URL" \
  --purchase-key "$GPT_IMAGE_PURCHASE_KEY" \
  --profile-name "alice" \
  --prompt "厚涂风格的幻想角色立绘，半身像" \
  --output output/portrait.png \
  --save-session
```

For image-to-image reserved generation, provide `--image /absolute/path/input.png`. The script converts it to a data URL before submitting the job.

## Common Options

- `--prompt`: Required for `generate`.
- `--image`: Optional image path or `data:image/...` URL for image-to-image.
- `--output`: Output PNG path, default `generated-image.png`.
- `--model`: Text model, default `gpt-5.4`.
- `--image-model`: Image model, default `gpt-image-2`.
- `--size`: Default `1024x1536`.
- `--quality`: Default `high`.
- `--output-format`: Default `png`.
- `--retries`: Direct official/proxy retry count, default `3`.
- `--timeout-ms`: Reserved job polling timeout, default `180000`.

Never place real secrets in the skill files. Pass them at runtime through environment variables, local shell variables, or the user's secret manager.
