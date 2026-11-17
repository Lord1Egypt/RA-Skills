Resolve the installed Skill root {baseDir} first. Script paths below are relative to that root, not the project or references directory.


# 550W Watermark & Text Eraser

<!-- 550w-capabilities:start -->
## Capabilities and inputs

- Image watermark removal: upload a user-selected image to erase a watermark or unwanted text.
- Local video subtitle and visual-watermark removal: upload a user-selected MP4/MOV video for processing. Erase the full frame by default; use pixel coordinates x1, y1, x2, y2 for a rectangle only when the user explicitly supplies them. Never guess coordinates.
- Video-link watermark removal: ask the user to choose Share → Copy link in the relevant app or platform website and provide the video/content share URL. TikTok and X are examples; actual support depends on the service response. Return the resolved platform-watermark-free video URL.
- If the agent cannot download the resolved video URL or the download times out, give the user the resolved data.video URL to download in a browser. Do not substitute the platform share URL or claim the file was downloaded. Successful resolution and client download are separate outcomes.
<!-- 550w-capabilities:end -->

Use this workflow only for media the user owns or is authorized to process. This Skill provides instructions; the actual processing is performed by 550W AI's remote MCP server.

If the MCP server is not connected, ask the user to add the Streamable HTTP endpoint `https://www.550wai.cn/mcp/global`. The first connection opens the 550W website for email sign-in and consent. Do not request a user number, API key, sub-key, password, or OAuth token. If the client cannot connect to remote OAuth MCP servers, explain the limitation and point to <https://eraser.550wai.com/agent/>. Never imply that a task ran when it did not.

## Workflow

1. Identify whether the request is for hardcoded subtitles, a supported public video-sharing link, or image watermark/text removal. Before upload or paid submission, tell the user that the media or link will be sent to 550W AI and that processing uses account credits. Reading credits and task status does not consume credits.
2. Use `query_credits` to check the balance. When the installed Agent can read the user's selected local file, run bundled scripts, and has Node.js 18+, pass JSON containing the absolute `filePath` and `mediaType` (image or video) on stdin to `node scripts/550w-upload.cjs inspect` to obtain the actual file size. Call remote `prepare_media_upload`, then pass the same path and type, `region:"global"`, `uploadUrl`, and `uploadTicket` on stdin to `node scripts/550w-upload.cjs upload`. Do not put the ticket in command-line arguments or logs; the script never reads an OAuth token. For subtitle removal, obtain the video's actual width, height, and duration, then call `estimate_subtitle_cost`; do not invent media properties. Submit with `submit_subtitle_task` and a stable 8–128 character `idempotencyKey`. On a timeout, check the task before retrying with the same inputs and key to avoid duplicate billing.
3. For a supported public video-sharing link, use `remove_video_watermark` with a stable 8–64 character `operationId`. Reuse that ID on retries. Supported sources and the final price are determined by the service response; do not promise support for an unverified platform.
4. For image watermark or text removal, inspect each selected image, then use `prepare_media_upload` to get a ticket. Include a stable 8–64 character `operationId` in the local `upload` input. The upload itself may create a billed task; use the returned `taskId` with `get_image_watermark_task`. If the upload response is lost, do not invent a new operation ID or blindly upload again. Process multiple images separately unless the tool explicitly supports a batch.
5. For subtitle jobs, use `get_subtitle_task` or `list_subtitle_tasks` to report progress. Before `delete_subtitle_task`, confirm the exact task with the user. Deletion does not imply a credit refund. While processing, provide the task ID and a way to check it later.

If credits are insufficient, direct the user to <https://eraser.550wai.com/purchase/>; do not purchase credits on their behalf. Account connections can be reviewed at <https://eraser.550wai.com/mcp-connect/>. This generic Skill package does not configure the remote MCP connection or grant local file/script access; those depend on the installed Agent. If the client cannot upload a local image or video, direct subtitle, visual-watermark, or image-watermark requests to <https://eraser.550wai.com/> for file upload. Do not treat a platform share link as a substitute for a local file or imply that processing succeeded. Share-link platform-watermark removal remains available when its tool works. Explain other tool or consent failures plainly.


Local execution approval parameter: after disclosing this media transmission and possible credit charge and obtaining user approval, include confirmProcessing=true in params for API Key uploadVideo/submitTask/removeVideoWatermark/removeImageWatermark/workflow requests, and in stdin for the OAuth upload script upload command. Missing or non-true values are rejected; never assume approval. Queries and inspect do not require it. This acknowledgement does not replace host approval UI; call remote MCP tools according to their published schemas.
