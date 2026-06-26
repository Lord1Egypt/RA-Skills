# ai-video-editor

Render-mode Sparki Business API skill with a Python-first, cross-platform workflow.

## Base URLs

- API base URL: `https://business-agent-api.sparki.io`

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup.py` | Create or validate `sparki.env` with Python standard library only |
| `scripts/health.py` | Check configuration and Business API reachability on macOS, Linux, or Windows |
| `scripts/edit_video.py` | Upload MP4, create render project, poll with exponential backoff, download final MP4 |
| `scripts/*.sh` | Legacy macOS/Linux wrappers that delegate to the Python entrypoints |

## Main Workflow

```bash
python scripts/edit_video.py <video_path> <tips> [user_prompt] [aspect_ratio] [duration]
```

Windows PowerShell:

```powershell
py -3 .\scripts\edit_video.py .\demo.mp4 22 "Create an energetic travel montage" 9:16 60
```

Examples:

```bash
python scripts/edit_video.py ./demo.mp4 22 "Create an energetic travel montage" 9:16 60
python scripts/edit_video.py ./demo.mp4 "" "Create a cinematic travel video with slow motion and dramatic pacing" 16:9 45
```

## Configuration

- Preferred: set `SPARKI_API_KEY` in the environment.
- Optional: store `SPARKI_API_KEY`, `SPARKI_API_URL`, and `SPARKI_OUTPUT_DIR` in `~/.openclaw/config/sparki.env`.
- `scripts/setup.py` can create the config file for you:

```bash
python scripts/setup.py
python scripts/health.py
```

## API Contract Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/business/assets/upload` | POST | Upload file with `files` |
| `/api/v1/business/assets/batch` | POST | Get asset status |
| `/api/v1/business/projects/render` | POST | Create render project |
| `/api/v1/business/projects/batch` | POST | Get render result |

This skill follows the Business API markdown contract rather than the current backend branch implementation.

## Polling Behavior

- Asset status polling uses exponential backoff starting at `ASSET_POLL_INTERVAL` (default `2`s), capped by `ASSET_POLL_MAX_INTERVAL` (default `30`s).
- Render status polling uses exponential backoff starting at `PROJECT_POLL_INTERVAL` (default `10`s), capped by `PROJECT_POLL_MAX_INTERVAL` (default `60`s).
- Timeouts remain controlled by `ASSET_TIMEOUT` and `PROJECT_TIMEOUT`.

## Platform Notes

- The primary implementation now depends only on Python standard library modules and supports macOS, Linux, and Windows.
- `curl`, `jq`, and `bash` are no longer required for the main workflow.
- Existing `.sh` files remain for Unix compatibility, but they are wrappers and not the primary interface.

## Troubleshooting

- Run `python scripts/health.py` first if the workflow fails before or during API calls.
- If `python` is unavailable on Windows, try `py -3`.
- If the issue persists, send details to support@sparksview.com.
