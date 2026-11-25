---
name: after-effects-motion-graphics
description: "Create After Effects-style motion graphics: title cards, lower thirds, kinetic typography, 3D extruded bevelled titles, shape layers with Trim Paths and Repeaters, Bezier motion paths, and animated charts."
version: 1.0.3
author: brajendrak00068
license: MIT
---

# After Effects Shape Layers, Keyframe Graph, and 3D Titles

Author After Effects-grade shape layers with Trim Paths, Repeaters, and SDF modifiers, spatial Bezier motion paths with auto-orient, graph-editor velocity easing, echo trails, and 3D extruded bevelled titles.

## Setup

This skill calls the Levea (livecore.ai) editing service, which requires a Levea account and API key.

1. Sign up and generate an API key at https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=after-effects-motion-graphics
2. Provide the key to the tool you use:
   - OpenClaw plugin `openclaw-ai-video-editor` (ClawHub): set `apiKey` in the plugin config.
   - MCP server `levea-mcp-server` (npm): set `LEVEA_API_KEY` in the MCP server config. `LEVEA_API_URL` is optional and defaults to `https://api.livecore.ai`.
3. Describe the edit you want in plain language; the tool returns a project ID and, after export, an MP4 URL.

## When to use

- Drawing vector shapes, custom SVG Bezier paths, arrows, underlines, and outlines onto the frame using arc-length Trim Paths.
- Building geometric bursts, echoed rings, and step-and-repeat grids with the After Effects Repeater (per-copy offset/scale/rotation, start-to-end opacity ramp) and shape modifiers (pucker & bloat, zig zag, wiggle paths, round corners, offset paths).
- Animating layers along curved spatial Bezier motion paths with auto-orient, graph-editor velocity/influence handles, layer echo motion trails, or posterize time.
- Creating real 3D extruded, bevelled hero titles with PBR materials (chrome, metal, glossy, glass, brushed metal), environment lighting, and 3D camera moves.

## Tool interface

Use the registered `ai-video-editor` (OpenClaw plugin) or `autonomous_edit` (MCP server) tool, or call `search_skills` / `load_skill` + `execute_action` / `execute_batch` for direct canonical control.

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
- `style_reference_url` (string, optional): A reference video whose editing style the result should match (pacing, captions, framing, zooms, transitions, grade).
- `skills` (array, optional): Your own saved skills (save_skill) to apply to this edit, as "user/<slug>" ids. Skills saved with apply: always are applied to every edit without being named.
- `flaggedIssues` (array, optional): Specific problems the user flagged that this run must fix.
- `brandId` (string, optional): Brand kit to apply to this call.
- `projectBrandId` (string, optional): Default brand kit for the project; persists across calls.
- `core_only` (boolean, optional): Return only rendering-essential scene fields (smaller responses).
<!-- edit-contract:end -->

### Example tool input

```json
{
  "prompt": "Open with a 3D extruded chrome title that says LAUNCH DAY with a dolly-in camera move, add a gold stroked circle with a 5-copy repeater that draws in via trim_end from 0 to 1 over 2 seconds, and export as MP4.",
  "project_id": "project_example_01"
}
```

## Capabilities

- Shape Layer Trim Paths & Repeater: arc-length trim start/end/offset, dash arrays, and repeaters with compounded per-copy offset, scale, rotation, anchor, and opacity ramp.
- Shape Modifiers: pucker & bloat, round corners, zig zag, wiggle paths, and offset paths.
- Keyframe Graph & Spatial Paths: value-space cubic Bezier velocity/influence easing, arc-length spatial motion paths with auto-orient, text range and wiggly selectors, layer echo ghost trails, and posterize time.
- Real 3D Extruded Titles: true extruded glyph geometry with customizable depth, bevel width/rings, 7 PBR materials, 5 environment lighting rigs, and 6 camera moves.

## Response fields

- `success` (boolean): True when the edit and verification passed.
- `status` (string): One of `completed`, `waiting`, `awaiting_approval`, or `failed`.
- `projectId` (string): Active project identifier for subsequent edits.
- `projectRevision` (number): Committed project revision number.
- `videoUrl` (string, optional): Rendered MP4 download URL when export completes.
- `verificationReport` (object): `status` is `verified`, `rejected`, `unverified`, or `not_applicable`, with each failed check and what repair tried.
- `qualityNotes` (array, optional): Advisory notes about the result.
- `jobId` (string, optional): Async render job identifier for status polling via `check_job_status`.
