---
name: ai-subtitle-remover
description: Remove hardcoded video subtitles, watermarks from short-video share links, and image watermarks or unwanted text with the 550W Open API; check processing tasks and credits. Use for user-selected media or public share links.
metadata:
  openclaw:
    primaryEnv: SUBTITLE_REMOVER_API_KEY
    requires:
      bins:
        - node
    envVars:
      - name: SUBTITLE_REMOVER_API_KEY
        required: false
        description: API key for authenticated requests to the 550W Open API.
      - name: SUBTITLE_REMOVER_USER_NO
        required: false
        description: User ID belonging to the same 550W account as the API key.
      - name: FFPROBE_PATH
        required: false
        description: Optional ffprobe executable path for inspecting public direct video URLs.
---

# 550W AI subtitle and watermark removal

Use the highest-level matching tool. The global edition defaults to English; its account setup uses Eraser, while media operations use the shared 550W Open API. Respond in the user's language when possible; tool messages fall back to English except for Chinese. Language never changes the service region.

## Credentials and data

- If credentials are missing, direct the user to the localized Eraser API page at `https://eraser.550wai.com/{locale}/api/`; use <https://eraser.550wai.com/api/> for English or unsupported locales. They need the User ID and API Key from the same account.
- In WorkBuddy, ask the user to fill in both fields in the connector settings. Otherwise use `SUBTITLE_REMOVER_USER_NO` and `SUBTITLE_REMOVER_API_KEY`, or the `configureCredentials` action. Never repeat a complete API Key.
- Before the first media operation, explain that the selected file or public link is sent to the 550W Open API. Use only a file the user explicitly selected or named. Privacy and terms: <https://eraser.550wai.com/privacy/> and <https://eraser.550wai.com/terms/>; localized pages are available.

## Capabilities

- Remove hardcoded subtitles from a local MP4/MOV video or a public direct video-file URL: `remove_video_subtitles` (CLI action `workflow`). The tool derives local-video metadata. `removeAudio` is only an optional parameter when explicitly requested.
- Remove a short-video watermark: ask the user to copy the public video share link inside the platform app and provide that link, or share text containing one link. TikTok and other service-supported platforms are examples. Call `remove_video_watermark` (CLI action `removeVideoWatermark`) with the share link; do not download the video first. Use a stable `operationId` when available.
- Remove watermarks or unwanted text from a user-selected local image: `remove_image_watermark` (CLI action `removeImageWatermark`). Process multiple images serially.
- Check subtitle or image task status, subtitle task history, and credit balance: `get_subtitle_task`, `get_image_task`, `list_subtitle_tasks`, `query_credits`.
- Delete an owned subtitle task: `delete_subtitle_task`. Explain that this schedules media cleanup and does not refund credits; confirm immediately before deletion.
- Ask one question if the input or intended billed operation is ambiguous.

If the host has no registered tools, send one JSON request on standard input to `node {baseDir}/dist/550w-skill.cjs`. Use an absolute `params.filePath` for a local file and parse the single JSON response.

## Processing and billing

- Subtitle removal uses full-frame erasing. Never request or send erase coordinates. For a public direct video URL, `ffprobe` obtains actual width, height, and duration unless all three are supplied. Reject private-network or credential-bearing URLs; never invent metadata.
- Use the same `subUserId` for a child user's submission, task lookup, list filtering, and deletion. The subtitle workflow polls for up to 10 minutes; on timeout or repeated query failure, return the task ID for later lookup.
- Image removal is synchronous by default. For `processing`, preserve the task ID and query it later. Only expose a result URL on `success`; explain `failed` and `expired` states.
- Subtitle removal is billed by duration and resolution. Share-link video watermark removal costs one credit per successful result; image removal costs 10 credits per successful image. State the unit before a batch and include only selected items.
- A timeout does not prove submission failed. Query the task first; never blindly retry a billed operation. Reuse an `idempotencyKey` only with identical subtitle inputs. Report the service's `refundStatus` on subtitle failure without assuming a refund.
- Return the result or actionable error to the user in every case.

Read [API contract](references/api-contract.md) for limits, statuses, billing formulas, and errors. Read [agent compatibility](references/agent-compatibility.md) for installation outside WorkBuddy.
