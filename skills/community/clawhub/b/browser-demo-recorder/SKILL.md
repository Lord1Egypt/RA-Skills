---
name: browser-demo-recorder
description: Record browser demo videos from a plain-language brief by turning the requested flow into a plan, driving the OpenClaw browser via CDP, encoding an MP4, writing the output into the workspace `media/` directory, and returning it with the MEDIA protocol. Use when the user wants a browser walkthrough, product demo, site recording, landing-page capture, hover/click/search flow recording, or asks to package browser recording into a reusable skill.
---

# Browser Demo Recorder

Turn a natural-language recording request into a deterministic browser recording that lands in the current workspace `media/` directory and can be sent back immediately.

## Workflow

1. Extract the recording brief into a concrete sequence.
2. Convert the sequence into a JSON plan.
3. Run `scripts/run-recording.mjs` against that plan.
4. Verify the MP4 exists in the current workspace `media/` directory.
5. Reply with a short status line and a `MEDIA:` line pointing at the generated file.

## What to Capture From the User Brief

Convert the request into these fields before recording:

- Start URL and any required destination URLs
- Viewport preference if given; otherwise use `1600x1200`
- Ordered steps: page holds, cursor sweeps, clicks, typing, scrolls, and ending frame
- Timing goals: total duration, per-step hold times, and any "don't click" / "hover only" constraints
- Output basename if the user hints at a name; otherwise derive a short slug from the task

If the brief is missing something critical, ask one question. Otherwise infer sensible defaults and proceed.

## Plan Format

Read `references/plan-schema.md` when building or debugging plans.

Use `references/example-skills-video-plan.json` as the default reference for a multi-step marketing demo with homepage, hub, search, and return-home flow.

## Runner

Run the recorder like this:

```bash
node scripts/run-recording.mjs /absolute/path/to/plan.json
```

Behavior:

- Connects to the existing OpenClaw browser via CDP
- Injects a visible cursor overlay so recordings show mouse position
- Uses human-like mouse movement, clicks, typing, and wheel-based scrolling
- Records directly to MP4
- Writes both MP4 and debug JSON into the plan's `outputDir`
- Default output directory should be the current workspace `media/` directory

## Output Rules

Always set the plan `outputDir` to the workspace media directory unless the user explicitly asks for a different safe location.

After success:

1. Mention the generated file path briefly.
2. Put the attachment on its own line using the MEDIA protocol.

Example reply shape:

```text
录好了，时长约 42 秒。
MEDIA:media/my-demo-2026-03-25T09-30-00-000Z.mp4
```

Use a workspace-relative `MEDIA:` path when possible.

## Implementation Notes

- Homepage forms sometimes open a new tab; if that breaks a continuous recording, add an `evaluate` step that changes the form target to `_self` before clicking submit.
- Prefer DOM-based targets over raw coordinates, but use coordinates for cinematic cursor sweeps.
- Keep cursor motion smooth and leave short holds after major transitions so the video is usable with voiceover.
- Save the generated plan near the media output or in a temp location only if you need to inspect it again; the MP4 in `media/` is the primary artifact.
- If the run fails, inspect the debug JSON written next to the output video before retrying.
