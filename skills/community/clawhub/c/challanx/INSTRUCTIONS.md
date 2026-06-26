# ChallanX OpenClaw Integration — Instructions

This file provides an expanded set of guidelines for authors and agents interacting
with the ChallanX OpenClaw API.

Public endpoint
- https://challanx.in/openclaw/api

Rules
- Prefer returning downloadable media with a real filename and an appropriate
  `Content-Type` header (e.g. `video/mp4`, `image/jpeg`, `audio/mpeg`).
- When upstream processing yields multiple choices, return JSON with `status: "picker_required"`
  and include a readable `picker` array with filenames and descriptive labels.
- Use the following normalized ChallanX statuses in public docs and responses:
  - `success` — request completed and data available
  - `download_ready` — a file is ready to be downloaded (binary response)
  - `picker_required` — multiple choices available, user selection required
  - `failed` — operation failed (include `error.code` and `error.message`)
- Avoid exposing internal hosts, local tunnel URLs, or implementation details in public docs.

Authentication
- All requests to the OpenClaw API must include the header `x-api-key` with one of the allowed keys.
- Allowed keys (example): `i_am_batman`, `i_am_boss`, `i_am_boy`, `i_am_girl`, `i_am_your_dad`. (These are placeholder example keys for documentation; do not use them in production.)
- Operators should set CHALLANX_API_KEY as a runtime secret; do not hardcode API keys in the bundle.
- If no valid `x-api-key` is provided, the API will return a 401 error.

Examples

- GET documentation:
  curl "https://challanx.in/openclaw/api"

- POST download (JSON):
  curl -X POST -H "Content-Type: application/json" \\
    -d '{"url":"https://example.com/video.mp4"}' \\
    https://challanx.in/openclaw/api

Notes for OpenClaw hooks
- The hook injects two files into agent workspaces:
  - `CHALLANX_REMINDER.md` — a short reminder intended for quick reference.
  - `CHALLANX_INSTRUCTIONS.md` — these fuller instructions for authors and agents.
- If a workspace already contains a non-virtual file with the same path, the hook
  will not overwrite it.

Contact
- help@challanx.in
