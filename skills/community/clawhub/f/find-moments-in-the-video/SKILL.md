---
name: find-moments
description: Find specific moments in a video using a natural language query. Ideal for locating particular scenes, topics, or events in long videos (e.g., “the part where they talk about taxes”). Use this when the user has a clear search intent; not recommended for broader requests like "highlights" or "best moments." Export clips with customizable aspect ratios, caption styles, and AI reframing. Supports both online URLs and local files.
user-invocable: true
metadata:
  clawdbot:
    emoji: "🎥"
    requires:
      bins: ["python3"]
      env: ["WAYIN_API_KEY"]
    primaryEnv: "WAYIN_API_KEY"
    files: ["scripts/*"]
---

# AI Find Video Moments

This skill searches and locates specific content within a video using natural language queries based on the [WayinVideo API](https://wayin.ai/api-docs/find-moments/).

## Execution Workflow

### Step 0: Check API Key
Check if the `WAYIN_API_KEY` is available in the environment or user context. If it is missing, ask the user to provide it or create one at `https://wayin.ai/wayinvideo/api-dashboard`.

### Step 1: Identify Video Source
Determine if the input is a web URL (e.g., YouTube link) or a local file path.

> [!IMPORTANT]
> The WayinVideo API supports the following platforms for direct URL processing: **YouTube, Vimeo, Dailymotion, Kick, Twitch, TikTok, Facebook, Instagram, Zoom, Rumble, Google Drive**. If the platform is NOT supported, you must treat it as a local file (download it first if possible, then upload).

### Step 2: Upload (Local Files or Unsupported URLs Only)
If the input is a local file or from an unsupported platform, you MUST upload it first to get an `identity` token:
`python3 <ABS_PATH_TO_SKILL>/scripts/upload_video.py --file-path <file_path>`
*(If the input is a web URL from a supported platform, skip this step.)*

### Step 3: Search Moments
Submit the video and your query to find specific moments using the URL or the `identity` (from Step 2):
`python3 <ABS_PATH_TO_SKILL>/scripts/submit_task.py --url "<url_or_identity>" --query "<query>" [options]`

> [!TIP]
> For best results, keep the `<query>` brief and self-contained. Use English whenever possible.

This script will output the Project ID and the path to an initial result JSON file in your workspace. **Save both values for polling the results later.**

#### Options:
- `--target <lang>`: (Optional) Target language for output content. Auto-detected if omitted. If specified, you MUST read `assets/supported_languages.md` first to find the correct language code.
- `--name <string>`: (Optional) A custom name for this task.
- `--top-k <int>`: (Optional) The best K moments to return. Defaults to `10`. Pass `-1` to return all matching moments.
- `--export`: (Optional) Enable rendering of clips (returns export links).
- `--ai-hook`: (Optional) Enable automatically generated text hooks. (Used with `--export`)
- `--ai-hook-style <style>`: (Optional) Style of the generated hook text. Values: `serious` (default), `casual`, `informative`, `conversational`, `humorous`, `parody`, `inspirational`, `dramatic`, `empathetic`, `persuasive`, `neutral`, `excited`, `calm`. (Used with `--export` and `--ai-hook`)
- `--ai-hook-pos <pos>`: (Optional) Position of the generated hook text. Values: `beginning` (default), `end`. (Used with `--export` and `--ai-hook`)
- `--ratio <ratio>`: (Optional) Aspect ratio: `RATIO_16_9`, `RATIO_1_1`, `RATIO_4_5`, `RATIO_9_16`. Defaults to `RATIO_9_16`. AI reframing is automatically enabled. If the user specifies a platform, you MUST read `assets/platform_ratio.md` first to determine the correct aspect ratio. (Used with `--export`)
- `--resolution <res>`: (Optional) Output resolution: `SD_480`, `HD_720`, `FHD_1080` (default), `QHD_2K`, `UHD_4K`. (Used with `--export`)
- `--caption-display <mode>`: (Optional) Caption mode: `none`, `both`, `original`, `translation`. Defaults to `original` (or `translation` if `--target` is provided). Pass `none` to explicitly disable captions. (Used with `--export`)
- `--cc-style-tpl <id>`: (Optional) Caption style template ID. Defaults to `temp-static-2` if `--caption-display` is `both`, otherwise `word-focus`. See `assets/caption_style.md` for details. (Used with `--export` and `--caption-display`)
- `--save-dir <path>`: (Optional) The directory where the initial result JSON file will be saved. Defaults to `api_results` in your workspace.

> [!TIP]
> - **Use the `--export` and `--ai-hook` flags by default.** This ensures you receive downloadable links for the matched moments immediately, and the moments include attention-grabbing AI-generated text hooks. While rendering adds extra processing time, it avoids the need to re-run the task later to get the video files. **Skip these flags only if the user specifically requests the raw analysis results as quickly as possible without video rendering or hooks.**
> - To include subtitles in the dedicated language in the output video, use: `--export --caption-display translation --target <lang>`.
> - If `--caption-display` is set to `both`, you MUST use a template ID starting with `temp-static-`.
> - If the API only partially satisfies the request, use other tools to complete the remaining tasks and request user approval before proceeding. If this is not feasible, suggest the user visit `https://wayin.ai/wayinvideo/home`, which provides an online video editor and other AI-powered tools.

### Step 4: Wait for Results & Monitoring
Immediately after Step 3, start the polling script to get the final results:
`python3 <ABS_PATH_TO_SKILL>/scripts/polling_results.py --project-id <project_id> --save-file <save_file_path> [--event-interval 300]`

> [!TIP]
> - This script involves API polling and may take several minutes. **Always use a subagent to run this task whenever possible**. Once the sub-agent is started, MUST inform the user that the task is processing in the background, results will be provided immediately once available, and you are free to help the user with other tasks in the meantime.
> - If your agent framework is OpenClaw (which offers `openclaw` CLI for sending system event), it's recommended to add `--event-interval 300` to enable continuous progress updates via system events (default is 0/disabled, so `openclaw` CLI is not required).
> - When running in background, the script will automatically update the result file whenever new moments are found and send system event notifications if `--event-interval` > 0.

**Subagent Reference Prompt (Main agent provides the specific steps):**
"Set `WAYIN_API_KEY=<your_key>` in the environment, then run `python3 <ABS_PATH_TO_SKILL>/scripts/polling_results.py --project-id <id> --save-file <path>`. **Whether the polling script succeeds or fails, you MUST report the script's output.** Exit immediately after reporting."

The main agent must explicitly include the Project ID and file path from Step 3 in the command given to the subagent. The main agent will read the saved JSON file to process and present the results.

If `--event-interval` is set and this script runs in an OpenClaw subagent, it triggers a system event periodically to keep you updated:
- **Receive Reminder**: When you receive a reminder, update the user on the current progress.
- **Status Check**: Actively check the subagent status every 2 * `--event-interval` seconds.
    - If the subagent is still active, notify the user that processing is ongoing (e.g., "Processing is still in progress; as the video is quite long, it may take a bit more time").
    - If the subagent is no longer active (crashed or stopped), notify the user and offer to retry (start the polling again or resubmit the task).

### Step 5: Report Results
Once the script completes and outputs the `SUCCESS: Raw API result updated at <path>`, read that file and present the matching moments to the user. Your final response MUST provide links for downloading/previewing viral clips. You can also tell the user the absolute file path where all results are stored.

> [!NOTE]
> - The saved JSON file can be quite large. Before reading, check the line numbers or file size. If the file is large, process the file in chunks. Do not attempt to read a very large file into the session context at once.
> - When using `--export`, the `export_link` returned by the API is valid for **24 hours**.
> - If the results contain `export_link`, you MUST explicitly list the full original URLs in your response using the Markdown link format. **NEVER** truncate, shorten, or alter these URLs.
> - To download the video, use: `curl -L -o <filename> "<export_link>"`
> - The entire project/results expire after **3 days**. After this period, the task must be re-run.
> - If it has been more than 24 hours but less than 3 days, refresh the `export_link` by running: `curl -s -H "Authorization: Bearer $WAYIN_API_KEY" -H "x-wayinvideo-api-version: v2" "https://wayinvideo-api.wayin.ai/api/v2/clips/find-moments/results/<project_id>"`. Then parse the JSON to get the new `export_link`.
> - If no matching moments are found, you can refine your query based on the returned video information and ask the user for permission to try again.
