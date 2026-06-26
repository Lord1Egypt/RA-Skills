---
name: comic-drama-generate
description: "Generate serialized comic-drama / 漫剧 episodes through a fixed multi-skill production pipeline with strong character consistency. Use when the user wants to create AI 漫剧, 连载短剧, animated short drama, or episodic short-form storytelling; when they need a repeatable 三视图→关键帧→图生视频 workflow for consistent characters; when they want to turn an idea into scripts, storyboards, 15-second single-shot videos, and final edited episodes; or when they want to combine video-prompt-generator, nano-banana-pro, sora-2-generate, and local ffmpeg for storyboard-to-video production."
---

# Comic Drama Generate

Use this skill to produce short comic-drama episodes through a deterministic, character-consistent pipeline.

## Required prerequisite skills

Require these skills before using this skill:

- `video-prompt-generator`
- `nano-banana-pro`
- `sora-2-generate`

If any are missing, install them first. Use this install pattern:

```bash
npx clawhub@latest install video-prompt-generator
npx clawhub@latest install nano-banana-pro
npx clawhub@latest install sora-2-generate
```

Before starting production, verify:

- all three prerequisite skill folders exist
- required API credentials are configured for the prerequisite skills
- `ffmpeg` is available locally
- there is enough credit/quota for script, image, and video generation

Credential note:

- `comic-drama-generate` orchestrates other skills and does not introduce its own separate API key.
- The prerequisite skills use their own environment-variable contract, typically `NANOPHOTO_API_KEY`.
- Prefer normal sub-skill execution that relies on the prerequisite skill's configured env.
- If direct script execution is necessary, first preserve the same env contract by ensuring `NANOPHOTO_API_KEY` is present in the shell.
- Use explicit `--api-key` only as a fallback when the shell cannot inherit the expected env.
- Do not treat direct reads from config files such as `openclaw.json` as the primary workflow; reserve them for debugging or recovery paths.

## Mandatory production order

Always follow this exact order.

1. **Ask the user for style first**
   - Ask for visual style before generating anything.
   - Also confirm tone, audience, episode count, target platform, aspect ratio, and approximate episode duration.
   - Lock the series bible first: premise, character roster, style keywords, and production constraints.

2. **Use `video-prompt-generator` to generate the script foundation**
   - Generate the story premise, dramatic arc, episode beats, and scene-level writing foundation.
   - Make the episode structure suitable for short-form serialized漫剧.
   - Keep the pacing compatible with downstream 15-second shot generation.

3. **Use `nano-banana-pro` to generate character turnarounds**
   - Generate character three-view sheets for all core recurring characters.
   - Treat the three-view sheets as the canonical identity source for face, hair, silhouette, wardrobe, and palette.
   - Do not skip this step when character consistency matters.

4. **Use `nano-banana-pro` to generate keyframes**
   - Generate keyframes for each planned shot using the turnaround image URLs as reference inputs.
   - For multi-character shots, include all relevant turnaround URLs.
   - Use keyframes to lock composition, costume continuity, environment cues, and emotional staging.

5. **Use `video-prompt-generator` to write the storyboard / shot script**
   - Convert each episode into shot-level prompts and a shot list.
   - Write for single-shot generation with clean handoff into video prompts.
   - Leave a hook at the end of every episode.

6. **Use `sora-2-generate` to create 15-second single-shot videos**
   - Default to 15-second shots unless the user explicitly wants a different supported duration.
   - Prefer `imageToVideo` for character shots.
   - Pass keyframe URLs as image inputs.
   - Use `textToVideo` only for shots where character consistency is unimportant, such as atmosphere inserts or environment transitions.

7. **Use local `ffmpeg` to trim, arrange, and merge clips**
   - Download and save each finished shot locally.
   - Trim or normalize clips locally if needed.
   - Merge shots in deterministic order with `ffmpeg`.
   - Export final episode cuts under a dedicated project directory.

## Non-negotiable working rules

- Prefer this consistency chain at all times:
  - character turnarounds → keyframes → image-to-video
- Use **public URLs**, not local file paths, when passing assets between:
  - character turnarounds → keyframes
  - keyframes → video generation
- Do **not** pass local files into `nano-banana-pro` or `sora-2-generate` APIs for these handoff steps.
- Do **not** skip directly from text prompt to final video for main character shots unless the user explicitly accepts weaker consistency.
- Keep exact turnaround and keyframe URLs recorded in project docs because downstream generation depends on them.
- Rewrite storyboard timing before generation if model limits, quota, or rate limits make the original plan unrealistic.

## Story and pacing guidance

- Design shots around the active video model's supported duration.
- For this workflow, prefer a shot grammar that fits 15-second single-shot clips.
- If an episode needs more time, split it into more shots rather than overloading one prompt.
- Ensure each episode ends with a hook, reveal, reversal, question, or emotional cliffhanger.

## Suggested project structure

```text
project/
  docs/
    series-bible.md
    episodes.md
    shot-list.md
    asset-urls.md
  assets/
    characters/
    keyframes/
  shots/
    ep01/
    ep02/
  edits/
  final/
```

## Execution notes

- Use `video-prompt-generator` twice when needed:
  - once for premise / episode writing
  - once for shot-level prompt refinement
- Use `nano-banana-pro` for both:
  - character turnaround generation
  - keyframe generation
- Use `sora-2-generate` mainly in `imageToVideo` mode for character-led shots.
- Use local `ffmpeg` for final editorial assembly, not remote editing tools.

## Expected deliverables

Produce organized outputs that make the project easy to resume:

- `docs/series-bible.md` — premise, style, characters, world rules
- `docs/episodes.md` — episode summaries and hook endings
- `docs/shot-list.md` — shot-by-shot structure for each episode
- `docs/asset-urls.md` — turnaround URLs, keyframe URLs, and video URLs
- local shot files under `shots/`
- local edit outputs under `edits/`
- final episode exports under `final/`

## Read these references when needed

- `references/workflow.md` — end-to-end production workflow
- `references/install-checklist.md` — prerequisite skill verification and install steps
- `references/asset-rules.md` — character turnaround, keyframe, and image-to-video consistency rules
