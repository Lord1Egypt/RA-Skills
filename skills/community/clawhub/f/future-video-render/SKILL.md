---
name: future-video-render
description: Create polished multi-shot videos with the Future Video Studio MCP, using either an account API key or no-account Link pay-per-render quotes. Use when an OpenClaw agent needs to submit a screenplay-driven render, quote and pay for a one-off render, attach public or local assets, poll until completion, cancel a running account job, download the final video, or return a finished signed video URL.
metadata: {"openclaw":{"homepage":"https://future.video/api-docs","mcpUrl":"https://mcp.future.video/mcp","manifest":"https://mcp.future.video/server.json","wellKnown":"https://mcp.future.video/.well-known/mcp-server.json","primaryEnv":"FVS_AGENT_API_KEY","optionalHeader":"X-FVS-Agent-Key","paidMode":"Link MPP pay-per-render"}}
---

# Future Video Render

Use this skill to create Future Video Studio renders through the hosted MCP server at `https://mcp.future.video/mcp`.

The MCP supports two billing paths:

- Account mode: send `X-FVS-Agent-Key` or configure `FVS_AGENT_API_KEY`; renders charge the owning Future Video Studio account wallet and require explicit user approval before submission.
- Pay-per-render mode: omit the API key, create a Link payment quote, pay the returned `payment_url`, then poll the claim-token status URL.

Fallback to the direct Agent API at `https://app.future.video/api/agent` only when the MCP client is unavailable or when a local-file workflow needs the bundled helper script.

## Best Fits

- multi-shot scene renders from a screenplay or creative brief
- custom productions that combine uploaded references, PDFs, and brand assets
- soundtrack-led music videos built around an uploaded song
- no-account one-off renders paid through Link for agents
- agent workflows that need a final signed video URL instead of loose clip outputs

## Before You Start

1. Connect to the MCP manifest at `https://mcp.future.video/server.json` or the remote endpoint at `https://mcp.future.video/mcp`.
2. If `FVS_AGENT_API_KEY` is available, treat it as a wallet-backed credential, not blanket permission to render.
3. Before account-mode submission, show the user the render summary, requested duration/resolution, any available estimate or budget cap, and ask for explicit approval to spend FVS wallet credits.
4. If no key is available or the user wants a visible price before paying, use pay-per-render mode with `fvs_create_paid_render_quote`.
5. Default the app origin to `https://app.future.video` unless a trusted local or staging FVS environment is explicitly configured.
6. Never ask the user for raw card details. Link payment authorization must happen through the returned Link/MPP payment URL or an approved agent payment tool.

## Quick Workflow

1. Build a render request object that matches the Future Video Studio payload.
2. Choose the billing path:
   - use `fvs_submit_render` for account/API-key mode only after explicit user approval to spend wallet credits
   - use `fvs_create_paid_render_quote` for no-account pay-per-render mode
3. For assets:
   - remote MCP clients should prefer public HTTPS `upload_urls`
   - local `upload_files` only work when the MCP server runs on the same machine as the agent
   - paid quote mode supports text-only requests and public HTTPS `upload_urls`, not local multipart file paths
4. Poll with the MCP status tools until the job reaches a terminal or review state.
5. Return `final_video_url` when available, or explain the blocking error if the render halts or fails.

## Example Prompts

- `Use $future-video-render to turn this 24-second product teaser brief and these brand reference files into a polished three-shot scene, then poll until the final video URL is ready.`
- `Use $future-video-render to create a moody four-shot music video from the uploaded track and lead character reference, keeping continuity consistent across the whole piece.`
- `Use $future-video-render without an FVS account key. Create a paid quote, let me approve the Link payment, then retrieve the final video.`
- `Use $future-video-render to submit a custom render that uses the uploaded style guide PDF, logo stills, and mood board images, then give me the finished signed video URL.`

## Preferred MCP Tools

Use the MCP tools first:

- `fvs_submit_render`: submit an account/API-key render
- `fvs_create_paid_render_quote`: create a no-account Link quote
- `fvs_get_render_status`: check account render status by `project_id` or `status_url`
- `fvs_get_paid_render_status`: check paid quote/render status by `status_url` or `quote_id` plus `claim_token`
- `fvs_cancel_render`: cancel an account-owned running render
- `fvs_download_final_video`: save a completed signed video URL

Account render:

```json
{
  "tool": "fvs_submit_render",
  "arguments": {
    "request": {
      "name": "Archive corridor test",
      "project_mode": "scene",
      "screenplay": "Shot 1: A woman enters a glowing archive corridor. Shot 2: She reaches toward a moving photograph. Shot 3: She steps through into a sunlit memory chamber.",
      "instructions": "Create exactly three cinematic shots totaling about 24 seconds. Keep the subject visually consistent. No subtitles or text overlays.",
      "shot_count": 3,
      "scene_target_duration_seconds": 24,
      "visual_style_preset": "realistic_cinematic",
      "video_resolution": "720p"
    },
    "poll_until_complete": false
  }
}
```

Paid quote render:

```json
{
  "tool": "fvs_create_paid_render_quote",
  "arguments": {
    "request": {
      "name": "Paid quote test",
      "project_mode": "scene",
      "screenplay": "Shot 1: A glass airship drifts over a frozen city.",
      "shot_count": 1,
      "scene_target_duration_seconds": 4,
      "video_resolution": "720p"
    }
  }
}
```

After a paid quote is created:

1. Keep the returned `payment_url`, `status_url`, `quote_id`, and `claim_token`.
2. Ask the user's Link-capable payment surface to approve/pay `payment_url`.
3. Poll with `fvs_get_paid_render_status` using `status_url`, or `quote_id` plus `claim_token`.
4. Return `final_video_url` after the paid render completes.

## Direct API Fallback

Use the bundled helper script only when MCP is unavailable or when account mode needs local multipart upload from the same filesystem. It handles multipart upload, auth headers, polling, and cancel/status URLs.

Submit and poll:

```powershell
python "{baseDir}/scripts/future_video_render.py" submit `
  --request-file request.json `
  --file character.png `
  --file soundtrack.wav `
  --poll `
  --write-json result.json
```

Check status later:

```powershell
python "{baseDir}/scripts/future_video_render.py" status --project-id proj_api_123
```

Cancel a running job:

```powershell
python "{baseDir}/scripts/future_video_render.py" cancel --project-id proj_api_123
```

If `python` is unavailable, read `{baseDir}/references/api.md` and use a direct HTTP request with the same endpoints and headers.

## Request Design Rules

- In account mode, always get explicit user approval before submitting a wallet-backed render, then send `X-FVS-Agent-Key` through the MCP secret header, local MCP environment, or direct API header.
- In paid quote mode, omit `X-FVS-Agent-Key` and use `fvs_create_paid_render_quote`.
- For direct account API fallback calls, send the render body as `multipart/form-data` with:
  - `request_json`: the JSON payload string
  - repeated `files`: optional uploaded files
- Use `project_mode` of `music`, `scene`, or `custom`.
- Prefer status polling over blocking waits. Use `wait_for_completion_seconds: 0` for direct API calls unless the user explicitly wants a short blocking wait.
- For uploaded soundtrack flows, set `music_workflow` to `uploaded_track` and upload at least one audio file.
- Keep `scene_target_duration_seconds` within `4` to `600`.
- Keep `shot_count` within `1` to `64`.
- Treat `final_video_url` as a signed URL that may expire. Return it promptly.

## Billing Alignment

- This skill does not introduce a separate API-only pricing model.
- Account API keys belong to a specific Future Video Studio account and charge that account's wallet balance.
- Do not submit account-mode renders merely because an API key is configured. Confirm the requested job and user-approved budget or spending intent first.
- Pay-per-render quotes use the same Future Video Studio credit estimate and return `amount_cents`, `currency`, and `credits_quoted` before payment.
- Future Video Studio applies the account's saved pipeline defaults before account renders run, so agent renders follow the same project configuration and credit model as in-product renders.
- Do not invent alternate pricing, discounts, or token math. Use the quote response or the account render status.

## Asset Handling

- When uploads need labels or purposes, add `assets[]` entries in `request_json`.
- Each `assets[]` entry should include:
  - `filename`
  - optional `label`
  - optional `purpose`
- `filename` must match the basename of the uploaded file.
- Use uploads for image references, mood boards, soundtrack files, source video, PDFs, or other supporting documents.
- Confirm that local files are intended to be shared with Future Video Studio before uploading them.
- Use public HTTPS `upload_urls` for remote MCP and paid quote mode.
- Use local `upload_files` only when the MCP server runs where the files exist, or use the direct helper script in account mode.

## Output Handling

After a submit or status check, inspect:

- `quote_id`
- `claim_token`
- `payment_url`
- `status`
- `current_stage`
- `is_running`
- `final_video_url`
- `last_error`

Treat the job as terminal when:

- `status` is `completed` or `failed`, or
- `current_stage` is `halted_for_review`, or
- the job is no longer running and there is no active queued/running state

When the response includes a finished `final_video_url`, give that URL back to the user with a short summary of what was rendered.

## Safety And Recovery

- Treat HTTP 402 from `render-quotes` as expected quote data, not a failure.
- Do not guess API keys, claim tokens, or payment credentials.
- Do not send `X-FVS-Agent-Key` to arbitrary hosts. The bundled helper only permits `https://app.future.video` by default and rejects full status/cancel URLs outside the configured FVS Agent API origin.
- Use `project_id`-derived status and cancel calls when possible. If using full `status_url` or `cancel_url`, use only URLs returned by Future Video Studio.
- For trusted local or staging FVS backends, the helper requires an explicit custom-host opt-in with `--allow-custom-host` or `FVS_ALLOW_CUSTOM_AGENT_HOST=1`.
- Do not retry paid quote payment blindly if approval fails; ask the payment surface or user to resolve the approval.
- Save `status_url` and `claim_token` from paid quote mode before payment so the result can be retrieved later.
- If a signed `final_video_url` expires, re-check status with the MCP status tool to obtain a fresh result URL.

## References

Read `{baseDir}/references/api.md` when you need:

- MCP endpoint and tool reminders
- the exact endpoint list
- payload field reminders
- example request bodies for `scene`, `music`, or `custom`
- OpenClaw config examples for account mode and paid quote mode

External references:

- `https://mcp.future.video/server.json`
- `https://mcp.future.video/.well-known/mcp-server.json`
- `https://future.video/api-docs`
