# easyimage-uploader

Upload local image files to an EasyImages 2.0 service and return the hosted image URL.

This skill is for OpenClaw / AgentSkills style workflows where the assistant should treat images as files and upload them to an EasyImages server through the official API.

## Features

- Upload local image files to EasyImages 2.0
- Return direct hosted image URLs
- Support skill-local `config.json`
- Support CLI flags and environment variables as fallback
- Support a config switch to avoid model-side image handling
- Support a configurable temp working directory

## Supported configuration

Create `config.json` in the skill root:

```json
{
  "server": "https://img.example.com",
  "token": "your-easyimage-token",
  "allow_model_image_input": false,
  "temp_dir": "./temp"
}
```

### Fields

- `server`: EasyImages base URL
- `token`: EasyImages upload token
- `allow_model_image_input`: whether upload requests are allowed to rely on model-side image understanding
  - `false`: prefer direct file-path handling and avoid unnecessary image analysis
  - `true`: allow model-side image handling when needed
- `temp_dir`: temporary working directory for downloaded or intermediate files
  - default recommended value: `./temp`

## Config priority

The uploader resolves config in this order:

1. CLI flags: `--server` and `--token`
2. Skill-local `config.json`
3. Environment variables:
   - `EASYIMAGE_URL`
   - `EASYIMAGE_TOKEN`

## Usage

Basic usage:

```bash
python3 scripts/upload_easyimage.py /absolute/path/to/image.jpg
```

Use a specific config file:

```bash
python3 scripts/upload_easyimage.py /absolute/path/to/image.jpg \
  --config /absolute/path/to/config.json
```

Override with explicit values:

```bash
python3 scripts/upload_easyimage.py /absolute/path/to/image.jpg \
  --server https://img.example.com \
  --token YOUR_TOKEN
```

## Example response

Successful upload returns normalized JSON like:

```json
{
  "ok": true,
  "http_status": 200,
  "result": "success",
  "code": 200,
  "url": "https://img.example.com/i/2026/04/16/example.jpg",
  "thumb": "https://img.example.com/app/thumb.php?img=/i/2026/04/16/example.jpg"
}
```

## EasyImages API notes

This skill uses the official EasyImages 2.0 upload endpoint:

- `POST /api/index.php`
- multipart form fields:
  - `image`
  - `token`

If the server returns `API Closed`, enable API upload in EasyImages first.

## Common failure cases

- `202`: upload quota reached
- `205`: blocked by allowlist / denylist rules
- `401`: login upload required by server policy
- `403`: invalid token or signature failure
- `406`: file type rejected
- `API Closed`: EasyImages API upload is disabled on the server

## Files

- `SKILL.md`: agent-facing skill instructions
- `scripts/upload_easyimage.py`: upload helper script
- `references/api.md`: upstream API notes
- `config.example.json`: config template

## Security notes

- Do not commit real `config.json` secrets to a public repository.
- Keep your EasyImages token private.
- If you want to minimize model-side image token usage, keep `allow_model_image_input` set to `false` and prefer file-path based workflows.

## License

This project is licensed under the MIT License.

See [`LICENSE`](./LICENSE) for the full terms.

EasyImages itself is a separate upstream project:

- Upstream: <https://github.com/icret/EasyImages2.0>
