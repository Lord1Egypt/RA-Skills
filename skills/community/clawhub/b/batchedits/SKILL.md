---
name: batchedits-video-editor
description: Autonomously edit videos, add captions, and remove silences via BatchEdits.
metadata:
  openclaw:
    primaryEnv: BATCHEDITS_API_KEY
    requirements:
    mcp:
      - batchedits
---

Turn your OpenClaw into an autonomous video editor using BatchEdits. Use when you need to add captions, remove silences, or apply custom styles to videos. Covers creating styles, uploading local videos, processing, and checking video status directly from WhatsApp, Telegram, or the CLI.

## Setup
1. Create an account at your BatchEdits instance.
2. Obtain your OAuth Client Token from the dashboard settings.
3. Provide your OAuth token to OpenClaw. You can do this securely by running:

```bash
openclaw config set env.BATCHEDITS_API_KEY client_xxxxx
```
*(Alternatively, you can `export BATCHEDITS_API_KEY=...` in your shell, or add it to the `.env` file in the folder where you run OpenClaw)*

4. Connect the BatchEdits MCP Server to your OpenClaw setup by running this in your terminal:

```
openclaw config set mcp.servers.batchedits '{"type": "sse", "url": "https://batchedits.com/api/mcp"}'
```

## Auth
The MCP server uses your `.env` key automatically. Under the hood, any direct HTTP uploads authenticate using standard OAuth 2.0:
```
Authorization: Bearer <BATCHEDITS_API_KEY>
```

### 1. Get Available Actions
Use the `list_actions` tool.

Returns an array of action templates (e.g., `remove_silence`, `add_captions`) with their `id`, `name`, and `description`. You need the `id` to build a style.

### 2. Create a Style
Use the `create_style` tool to build a reusable video editing preset.

Arguments:
- `name`: e.g. "Silence Remover"
- `actions`: JSON string of templates (e.g., `[{"id": "action_123"}]`)

Returns the new `styleId`.

### 3. Upload Video
Use the `upload_videos` tool.

Arguments:
- `filePaths`: Array of absolute paths (e.g., `["/path/to/local/video.mp4"]`)

Because video files are large binaries, this tool returns a ready-to-run `curl` command. **You must execute the returned curl command in your terminal** to upload the local file to the server. Parse the JSON output of the curl command to get the new `videoId`.

### 4. Process Video
Use the `process_video` tool to start the edit.

Arguments:
- `videoId`: The ID from step 3
- `styleId`: The ID from step 2

### 5. Check Results
Use the `list_videos` tool.

Returns a list of your videos with their current status: `pending`, `processing`, `completed`, or `failed`.

## Recommended Workflow for Video Editing
1. Identify the local video file provided by the user (e.g., downloaded from Telegram).
2. Determine the requested edits (captions, silence removal, etc.).
3. Check `get_styles` to see if a matching style already exists. If not, use `list_actions` and `create_style` to make one.
4. Call `upload_videos` to get the upload command.
5. Execute the `curl` upload command and extract the `videoId`.
6. Call `process_video` to start the job on the remote server.
7. Inform the user that the video is processing.
8. Call `list_videos` to check when the video reaches `completed` status.

## Tips
- Always check `get_styles` first. Reusing existing styles is faster than creating a new one every time!
- Uploading videos is handled via `curl` because OpenClaw needs to stream large local binaries to the remote server efficiently.
- You can queue multiple videos to the same style for bulk processing by repeating the upload & process steps!
