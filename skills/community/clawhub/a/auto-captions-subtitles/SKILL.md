---
name: auto-captions-subtitles
description: "Generate synchronized word-by-word animated captions and translated subtitles for video timelines."
version: 1.0.4
author: brajendrak00068
license: MIT
---

# Auto Captions and Subtitles

Generate synchronized word-by-word animated captions and translated subtitles for video timelines.

## Setup

This skill calls the Levea (livecore.ai) editing service, which requires a Levea account and API key.

1. Sign up and generate an API key at https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=auto-captions-subtitles
2. Provide the key to the tool you use:
   - OpenClaw plugin `openclaw-ai-video-editor` (ClawHub): set `apiKey` in the plugin config.
   - MCP server `levea-mcp-server` (npm): set `LEVEA_API_KEY` in the MCP server config. `LEVEA_API_URL` is optional and defaults to `https://api.livecore.ai`.
3. Describe the edit you want in plain language; the tool returns a project ID and, after export, an MP4 URL.

## When to use

- Generating word-level synchronized captions from a video audio track.
- Styling subtitles with built-in typography presets such as karaoke or pill highlights.
- Translating timeline captions into another language.

## Tool interface

Use the registered `ai-video-editor` (OpenClaw plugin) or `autonomous_edit` (MCP server) tool to run edits against a project timeline.

### Tool parameters

<!-- edit-contract:start (generated from contract/edit-contract.json — edit that file, then run node scripts/sync-contract.mjs) -->
- `prompt` (string, required): Description of the video edit to perform, in the user's own words.
- `project_id` (string, optional): Project identifier returned by a prior call; reuse it for every follow-up edit on the same video.
- `video_url` (string, optional): Public source video URL when starting a new project.
- `assets` (array, optional): Input media (video, image, audio) as public HTTP/HTTPS URLs.
- `scene` (object, optional): Existing scene/timeline state to continue editing (advanced).
- `captionTemplatePreset` (string, optional): Caption template id to apply: a builtin slug (e.g. `hormozi`, `viral-pop`, `karaoke`) or a saved template id. With the MCP server, `list_caption_templates` lists the exact ids; elsewhere, name the look in the prompt.
- `captionTemplateMode` (string, optional): How to apply `captionTemplatePreset`: one of `add`, `recreate`, `style`, `translate`, `clear`, `remove_fillers`.
- `requirePlanApproval` (boolean, optional): When `true`, pause after planning and return `workingMemory` for the user to approve.
- `workingMemory` (object, optional): State returned by a paused plan-approval call; send it back to resume.
- `editedPlan` (object, optional): The user's edited version of a plan returned by an approval pause.
- `planDecision` (string, optional): Set to `"approve"` to approve the plan from an approval pause; resend it with that response's `workingMemory`.
- `attachedImages` (array, optional): Reference image URLs for planning (style, branding).
- `flaggedIssues` (array, optional): Specific problems the user flagged that this run must fix.
- `brandId` (string, optional): Brand kit to apply to this call.
- `projectBrandId` (string, optional): Default brand kit for the project; persists across calls.
- `core_only` (boolean, optional): Return only rendering-essential scene fields (smaller responses).
<!-- edit-contract:end -->

### Example tool input

```json
{
  "prompt": "Generate word-by-word captions at the bottom of the frame using the viral-pop preset.",
  "project_id": "project_example_01"
}
```

## Capabilities

- Speech-to-text word timing alignment on the active timeline.
- 60+ caption templates including Hormozi, Spotlight, karaoke, word-pill, phrase lockups, and two-line podcast looks.
- Animated word entrances and burn-aways; Latin, Indic, Arabic, Cyrillic, and Greek text.
- Safe-zone placement that avoids covering faces and lower-third graphics.
- Multi-language subtitle translation.

## Response fields

- `success` (boolean): True when the edit and verification passed.
- `status` (string): One of `completed`, `waiting`, `awaiting_approval`, or `failed`.
- `projectId` (string): Active project identifier for subsequent edits.
- `projectRevision` (number): Committed project revision number.
- `videoUrl` (string, optional): Rendered MP4 download URL when export completes.
- `verificationReport` (object): `status` is `verified`, `rejected`, `unverified`, or `not_applicable`, with each failed check and what repair tried.
- `qualityNotes` (array, optional): Advisory notes about the result.
- `jobId` (string, optional): Async render job identifier for status polling via `check_job_status`.
