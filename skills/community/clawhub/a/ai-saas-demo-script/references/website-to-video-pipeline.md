# Website To Video Pipeline

Use this reference when turning a real website, product URL, local HTML file, or web app into an AI SaaS product demo video. It is inspired by website-to-video agent pipelines such as HyperFrames, but keep the output framework-neutral: Remotion, HyperFrames, HTML/GSAP, or another renderer can all use the same creative pipeline.

## Core Idea

Do not start by inventing scenes. Start by capturing the product:

```text
capture product reality
-> extract brand and UI signals
-> identify workflow/value path
-> write storyboard
-> choose implementation strategy
-> build composition
-> snapshot key frames
-> render final video
```

The capture step prevents generic demo videos. The snapshot step prevents layout mistakes.

## Inputs

Accept any of these:

- public product URL
- local HTML file
- local dev server URL
- screenshot set
- Figma export
- product repo with runnable app
- existing Remotion/HTML video project

Ask for missing credentials only if the target product cannot be reached. If the product is private but a static HTML or screenshots are available, proceed from those.

## Pipeline

| Step | Output | What to do |
|---|---|---|
| 1. Capture | Screenshots, DOM text, colors, fonts, assets, sections, CTAs | Inspect the real UI before scripting. |
| 2. Product analysis | Workflow map and value hypothesis | Identify who the user is, what they do, what changes, and what result proves value. |
| 3. Script | Short on-screen copy | Use outcome-led copy, 2-7 words per beat. |
| 4. Storyboard | Shot table with time, visual, text, motion, purpose | Map each shot to a product state change. |
| 5. Implementation choice | Screenshot, layered UI, HTML composition, or hybrid | Choose based on precision needs. |
| 6. Build | Renderable composition | Implement UI, motion, data, captions, audio. |
| 7. Snapshot QA | Key still frames | Check alignment, overlap, readability, and camera target. |
| 8. Render | MP4 and key frames | Export final video and review deliverables. |

## Capture Checklist

Capture or inspect:

- full-page screenshots at key scroll depths or app states
- viewport screenshots at the final video aspect ratio
- visible text in reading order
- navigation labels and primary CTAs
- brand colors and accent colors
- font families and weights
- icons, logos, media, SVGs, Lottie, video assets
- product data shown in tables, dashboards, cards, charts
- interactive states: empty, loading, selected, generated, approved, completed
- trust cues: owner, status, timestamp, permissions, risk, audit, approval

For local HTML, inspect the file structure and render it in a browser when possible. For a repo, find the route, run command, and target viewport before capture.

## Product Analysis Questions

Answer these before writing the storyboard:

```text
Who is the user?
What job are they trying to complete?
What input starts the workflow?
What does the AI extract, generate, match, score, or prepare?
Where does the human review or approve?
What visible result proves completion?
What 2-3 metrics or benefits matter most?
Which UI object can carry continuity across scenes?
```

Prefer a real workflow over a feature tour. A good demo has a path:

```text
input -> AI transformation -> review/control -> result -> value
```

## Implementation Strategy

Choose the lightest strategy that supports the needed precision:

| Strategy | Use when | Risk |
|---|---|---|
| Screenshot context | Broad page context or quick establishing shot | Focus boxes and overlays may drift. |
| Layered UI reconstruction | Precise cursor, focus, data, foreground card, camera motion | More build time, better control. |
| HTML/GSAP composition | Fast website-style video, agent-friendly HTML animation | Requires deterministic timeline discipline. |
| Hybrid | Screenshot background with layered foreground UI | Good for speed, but verify alignment carefully. |

Default for polished AI SaaS demos: use layered UI for active product operations and screenshots only for broad context.

## Storyboard Rules

Each storyboard row must include:

- product state
- viewer focal target
- user or AI action
- motion/transition reason
- value proof

Bad:

```text
Show dashboard with nice animation.
```

Good:

```text
Cursor selects the client row; the row lifts into a foreground card while the camera pushes toward the analysis panel.
```

## Composition Rules

For Remotion:

- Follow `remotion-layered-ui-checklist.md`.
- Use TypeScript checks before render.
- Render key frames before final video.
- Keep all focus/cursor/data animations attached to components.

For HTML/GSAP or HyperFrames-style composition:

- Use deterministic timelines.
- Avoid `Math.random()` unless seeded.
- Register timelines so the renderer can seek frames.
- Do not fetch asynchronously during timeline construction.
- Give timed elements explicit start/duration metadata.
- Add entrance animation to every scene and a reasoned transition between scenes.

For either framework:

- Keep 1920x1080 and 30fps unless the user asks otherwise.
- Use real product copy only where it supports the workflow.
- Replace dense paragraphs with short captions or visible status labels.
- Avoid decorative sweeps, generic glow, and static perspective.

## Snapshot QA

Before final render, export still frames for:

```text
0-2s hook
first product UI entrance
first real operation
AI transformation
data/result reveal
human review or approval
final value/outro
```

For each frame, check:

- no caption/UI overlap
- focus target precise
- cursor not covering readable text
- overlay not blocking required content
- data and status readable
- camera target obvious
- no effect exists only as decoration

If a frame fails, fix the composition before rendering the MP4.

## Output Folder Convention

Use a clear output structure:

```text
output/
  product-demo-vN.mp4
  vN-open-030.png
  vN-operation-150.png
  vN-data-900.png
  vN-approval-1500.png
  storyboard.md
```

Update the storyboard when the implemented video changes.

## Final Response Format

When reporting completion, include:

1. what product/workflow was captured
2. what implementation strategy was used
3. what scenes changed
4. what QA was run
5. links to MP4 and key frames
6. the next best iteration options

Keep the response short. The render and key frames are the proof.
