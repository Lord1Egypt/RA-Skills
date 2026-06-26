---
name: easyimage-uploader
description: Upload local image files to an EasyImages 2.0 service and return the hosted image URL. Use when the user asks to upload an image, host a picture, put a local screenshot/photo onto an EasyImages server, or wants a sharable image link generated from a local file. This skill supports skill-local configuration via config.json, with CLI flags or environment variables as fallback.
---

# easyimage-uploader

Upload a local image to an EasyImages 2.0 server, then return the hosted image URL.

## Configuration priority

Resolve configuration in this order:

1. CLI flags: `--server` and `--token`
2. Skill-local config file: `config.json`
3. Environment variables fallback:
   - `EASYIMAGE_URL`
   - `EASYIMAGE_TOKEN`

Recommended setup: create `config.json` in the root of this skill.

Example:

```json
{
  "server": "https://img.example.com",
  "token": "your-easyimage-token",
  "allow_model_image_input": false,
  "temp_dir": "./temp"
}
```

A template file is included as `config.example.json`.

## Config fields

- `server`: EasyImages service base URL
- `token`: EasyImages upload token
- `allow_model_image_input`: whether upload requests are allowed to rely on model-side image understanding
  - `false`: prefer direct file-path upload only, avoid image analysis, avoid vision tool usage
  - `true`: model-side image handling is allowed when needed
- `temp_dir`: temp working directory for this skill
  - default recommended value: `./temp`
  - relative paths are resolved relative to this `SKILL.md` / skill root directory
  - with the default, the effective directory is `easyimage-uploader/temp/`

If configuration is missing, stop and ask the user for the missing value.

## Workflow

1. Confirm which local image file should be uploaded.
2. Read `references/api.md` if you need the exact upstream API shape or status meanings.
3. Read `config.json` when behavior matters.
4. If `allow_model_image_input` is `false`, do not use image analysis or vision tools just to understand image content. Treat the image as a file and upload by path only.
5. Use `temp_dir` for temporary files when downloads, conversions, or intermediate storage are needed. If the directory does not exist, create it first.
6. Prefer absolute paths for both the script and the image file. Do not rely on `~` expansion in generated commands. Safe default:

```bash
python3 /absolute/path/to/skills/easyimage-uploader/scripts/upload_easyimage.py /absolute/path/to/image
```

7. If needed, point to a specific config file with an absolute path:

```bash
python3 /absolute/path/to/skills/easyimage-uploader/scripts/upload_easyimage.py /absolute/path/to/image \
  --config /absolute/path/to/config.json
```

8. If needed, override with explicit CLI values:

```bash
python3 /absolute/path/to/skills/easyimage-uploader/scripts/upload_easyimage.py /absolute/path/to/image \
  --server https://img.example.com \
  --token YOUR_TOKEN
```

9. The bundled script normalizes `~` and relative paths for the image and config arguments, but still prefer absolute paths in examples and real executions to avoid shell-specific surprises.
10. Parse the JSON output.
11. If `ok` is true, return the `url` to the user. Mention `thumb` only if useful.
12. Do not expose `delete_url` unless the user explicitly asks for deletion capability.
13. If upload fails, explain the likely cause using the `code` or error payload.

## Failure handling

When the script returns a failure payload:

- `network_error`: server unreachable, DNS/TLS/network problem, or timeout
- `http_error`: server returned a non-2xx HTTP response
- `invalid_json`: server responded unexpectedly
- EasyImages `code` values should be interpreted using `references/api.md`

Common user-facing explanations:

- `202`: server-side upload quota reached
- `205`: current client is blocked by EasyImages allow/deny rules
- `401`: server requires login uploads instead of token-only uploads
- `403`: token invalid or signature check failed
- `406`: file type rejected

## Notes

- Use this skill for local files that already exist on disk.
- If the user only gives a remote URL and wants it mirrored, download it first only if appropriate and allowed.
- Prefer returning the direct image `url` as the main result.
- Keep secrets safe. Never echo the configured token back to the user.
- `config.json` contains secrets. Keep file permissions tight and avoid committing it to public repositories.
