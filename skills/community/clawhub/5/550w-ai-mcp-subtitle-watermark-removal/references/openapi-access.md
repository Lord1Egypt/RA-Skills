Resolve the installed Skill root {baseDir} first. Script paths below are relative to that root, not the project or references directory.


# 550W Watermark & Text Eraser

<!-- 550w-capabilities:start -->
## Capabilities and inputs

- Image watermark removal: upload a user-selected image to erase a watermark or unwanted text.
- Local video subtitle and visual-watermark removal: upload a user-selected MP4/MOV video for processing. Erase the full frame by default; use pixel coordinates x1, y1, x2, y2 for a rectangle only when the user explicitly supplies them. Never guess coordinates.
- Video-link watermark removal: ask the user to choose Share → Copy link in the relevant app or platform website and provide the video/content share URL. TikTok and X are examples; actual support depends on the service response. Return the resolved platform-watermark-free video URL.
- If the agent cannot download the resolved video URL or the download times out, give the user the resolved data.video URL to download in a browser. Do not substitute the platform share URL or claim the file was downloaded. Successful resolution and client download are separate outcomes.
<!-- 550w-capabilities:end -->

Use the highest-level matching tool. The global edition defaults to English; its account setup uses Eraser, while media operations use the shared 550W Open API. Respond in the user's language when possible; tool messages fall back to English except for Chinese. Language never changes the service region.

## Credentials and data

- If credentials are missing, direct the user to the localized Eraser API page at `https://eraser.550wai.com/{locale}/api/`; use <https://eraser.550wai.com/api/> for English or unsupported locales. They need the User ID and API Key from the same account.
- This OpenAPI edition uses `SUBTITLE_REMOVER_USER_NO` and `SUBTITLE_REMOVER_API_KEY`; WorkBuddy's separate remote connector uses website OAuth. Before using `configureCredentials`, explain that it verifies credentials with 550W and saves the User ID and API Key to the local user configuration directory; set `confirmCredentialStorage=true` only with the user's agreement. Prefer environment credentials or OAuth on shared hosts. Never repeat a complete API Key.
- Before the first media operation, explain that the selected file or public link is sent to the 550W Open API. Use only a file the user explicitly selected or named. Privacy and terms: <https://eraser.550wai.com/privacy/> and <https://eraser.550wai.com/terms/>; localized pages are available.

## Capabilities

- Remove hardcoded subtitles or visual watermarks from a local MP4/MOV video or a public direct video-file URL: `remove_video_subtitles` (CLI action `workflow`). The tool derives local-video metadata. `removeAudio` is only an optional parameter when explicitly requested.
- Remove a short-video watermark: ask the user to copy the public video share link inside the platform app and provide that link, or share text containing one link. TikTok and other service-supported platforms are examples. Call `remove_video_watermark` (CLI action `removeVideoWatermark`) with the share link; do not download the video first. Use a stable `operationId` when available.
- Remove watermarks or unwanted text from a user-selected local image: `remove_image_watermark` (CLI action `removeImageWatermark`). Process multiple images serially.
- Check subtitle or image task status, subtitle task history, and credit balance: `get_subtitle_task`, `get_image_task`, `list_subtitle_tasks`, `query_credits`.
- Delete an owned subtitle task: `delete_subtitle_task`. Explain that this schedules media cleanup and does not refund credits; confirm the exact task ID immediately before deletion, then pass `confirmDeletion: true`. Never infer confirmation from the original processing request.
- Ask one question if the input or intended billed operation is ambiguous.

If the host has no registered tools but can run Node.js 18+ and read the user's selected file, send one JSON request on standard input to `node {baseDir}/dist/550w-skill.cjs`. Use an absolute `params.filePath` for a local file and parse the single JSON response. Installing the Skill does not itself grant script execution or file access. If the client cannot read or upload a local image or video, direct the user to <https://eraser.550wai.com/> for file upload; do not substitute a platform share link for a local file or claim processing succeeded. Share-link watermark removal remains a separate option when available.

## Processing and billing

- Video erasing defaults to the full frame. Only pass all four rectangle coordinates if the user explicitly provides them. For a public direct video URL, `ffprobe` obtains actual width, height, and duration unless all three are supplied. Reject private-network or credential-bearing URLs. When probing a link, redirects are rejected; ask for the final direct video-file URL. If all metadata is supplied, the Skill checks the URL's public address but does not probe redirects; the service still validates the submitted source. Never invent metadata.
- Use the same `subUserId` for a child user's submission, task lookup, list filtering, and deletion. The subtitle workflow polls for up to 10 minutes; on timeout or repeated query failure, return the task ID for later lookup.
- Image removal is synchronous by default, but a response may still contain an in-progress task. Preserve its task ID and query it later. Only expose a result URL on `success`; explain `failed` and `expired` states. Treat an unknown image status as unfinished, not completed.
- Subtitle removal is billed by duration and resolution. Share-link video watermark removal costs one credit per successful result; image removal costs 10 credits per successful image. State the unit before a batch and include only selected items.
- A timeout or server error does not prove a billed submission failed. Query the task or check the original operation first; never blindly retry it. Read-only queries may be retried later. Reuse an `idempotencyKey` only with identical subtitle inputs. Report the service's `refundStatus` on subtitle failure without assuming a refund.
- If the service explicitly reports insufficient credits, give the response's `purchaseUrl` to the user. The global purchase page is <https://eraser.550wai.com/purchase/> or its supported `/{locale}/purchase/` variant. Do not treat an ordinary authentication failure as a purchase prompt; do not buy credits on the user's behalf.
- Return the result or actionable error to the user in every case.

Read the bundled `references/api-contract.md` for limits, statuses, billing formulas, and errors, and `references/agent-compatibility.md` for local installation. For web readers, the same files are available as [API contract](https://github.com/sunshinehu/550w-ai-subtitle-remover/blob/main/references/api-contract.md) and [agent compatibility](https://github.com/sunshinehu/550w-ai-subtitle-remover/blob/main/references/agent-compatibility.md).


Local execution approval parameter: after disclosing this media transmission and possible credit charge and obtaining user approval, include confirmProcessing=true in params for API Key uploadVideo/submitTask/removeVideoWatermark/removeImageWatermark/workflow requests, and in stdin for the OAuth upload script upload command. Missing or non-true values are rejected; never assume approval. Queries and inspect do not require it. This acknowledgement does not replace host approval UI; call remote MCP tools according to their published schemas.
