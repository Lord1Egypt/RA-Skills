# End-to-end workflow

## 1. Preflight

- Ask for the user's preferred visual style first.
- Confirm:
  - genre / style
  - tone
  - episode count
  - episode duration target
  - target platform and aspect ratio
  - whether every episode should end with a hook
- Confirm prerequisite skills are installed.
- Confirm credentials and quota are ready.
- Prefer normal sub-skill execution that uses the prerequisite skills' configured env.
- If using direct script execution via `exec`, preserve the same env contract first by ensuring `NANOPHOTO_API_KEY` is available in the shell; only fall back to `--api-key` when needed.
- Confirm `ffmpeg` is installed locally.
- Create a dedicated project folder.

## 2. Script foundation

Use `video-prompt-generator` to produce:
- premise expansion
- episode arcs
- story beats
- scene language
- hook phrasing for each episode ending

Keep the script compatible with 15-second single-shot downstream generation.

## 3. Character asset development

Use `nano-banana-pro` to create:
- protagonist three-view sheets
- antagonist three-view sheets
- important support character three-view sheets
- recurring creature/object identity sheets when needed

Always preserve the final public asset URLs.

## 4. Keyframe development

For each shot:
- identify which characters appear
- pass their turnaround URLs as input references
- generate a strong keyframe
- optionally generate start/end keyframes if motion planning needs it

Use URLs as handoff inputs. Do not rely on local paths for API handoff.

## 5. Storyboard refinement

Use `video-prompt-generator` again to produce:
- shot list
- shot-by-shot prompt language
- pacing suitable for 15-second clips
- final-shot hook framing for each episode

## 6. Video generation

Use `sora-2-generate`:
- prefer `imageToVideo` for character-led shots
- pass keyframe URLs as image inputs
- default to 15-second single-shot clips
- reserve `textToVideo` for non-character inserts or low-consistency shots

## 7. Editing

- Download every shot locally
- Trim or normalize clips if needed
- Create concat lists
- Merge with `ffmpeg`
- Export the episode to `final/`

## 8. Iteration

If character drift appears:
- improve turnarounds first
- regenerate keyframes second
- regenerate video clips last

Do not try to fix severe consistency drift only by rewriting the video prompt.
