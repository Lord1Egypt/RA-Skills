---
name: cliptude
description: Generate Cliptude videos from a saved template using the cliptude CLI or MCP. Use when the user wants a video from a topic, a custom script, an uploaded voiceover file, or a talking-head recording (same as create.html). If they asked only for a script or only for narration audio, use create_script / cliptude script or create_voiceover / cliptude voiceover instead of create_job. To turn that completed job into an MP4, use continue_job / cliptude continue (same job id). If they only gave a topic or title for a video, follow cliptude-script first — never pass the title as --prompt. If they have narration audio, pass --voiceover / voiceover_path and skip cliptude-script. If they have a presenter video, pass --talking-head / talking_head_path with a Talking Head template.
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: CLIPTUDE_API_KEY
    envVars:
      - name: CLIPTUDE_API_KEY
        required: false
        description: Cliptude API key from cliptude.com/developers. Not needed if you connect the MCP server at https://mcp.cliptude.com/mcp or run `cliptude auth login`.
    emoji: "🎬"
    homepage: https://cliptude.com
---

# Cliptude video generation

**Want to direct every visual yourself** (theme, colours, every motion graphic and its text and timing, the search
query, person or URL behind every shot)? On a Faceless Documentary, Faceless Top 10 or Avatar Video template, follow
**cliptude-plan**: `create_plan_job` → `get_narration` → `get_kind_catalog` → `check_plan` → `lock_plan` →
`continue_job` → `get_plan_review` (revise on the same job if needed) → `render_project`. Cliptude then only voices,
sources and renders your plan.

Style lives in a **saved template** (voice, model, format). Either the user finishes the Cliptude wizard once and clicks **Save as template**, or you create one with `cliptude template-create` / MCP `create_template` (see `template-options` / `get_template_options` for fields and `voices` / `list_voices` for voice_id).

## Before generate — prompt vs script vs voiceover vs talking head

Same modes as create.html. **Exactly one narration source.** Prompt and script may be sent together (script is voiced; prompt is extra context). A voiceover or talking-head file cannot be combined with prompt, script, or each other.

**Never pass the video title as `--prompt` / `prompt`.** Production researches the topic, then writes narration. Copying the title into prompt skips that and yields a thin video.

| User gave you… | Do this |
|---|---|
| Topic or title only (“make a video about X”) | Follow **cliptude-script**: web-search, write spoken narration, then `--script-file` / `script` |
| Full narration they want voiced | `--script` / `--script-file` as-is (spoken words only) |
| Explicit “let Cliptude write the script” | `--prompt` = a **brief** (audience, angle, must-include facts) — not the title |
| A voiceover audio file (MP3, M4A, WAV, …) | `--voiceover path` / MCP `voiceover_path`, or a public link as `--voiceover-url` / `voiceover_url` (remote hosts cannot send a local file). Cliptude transcribes it and skips TTS. Do not also pass `--prompt` or `--script`. Do not run **cliptude-script**. Duration comes from the file, which must be at least 6 minutes long. |
| A talking-head presenter video (MP4, MOV, WEBM, AVI) | `--talking-head path` / MCP `talking_head_path` with a **Talking Head** template. Cliptude transcribes it and skips TTS. Do not also pass `--prompt`, `--script`, or `--voiceover`. Do not run **cliptude-script**. Duration comes from the file, which must be at least 6 minutes long. |

Read `../cliptude-script/SKILL.md` before `generate` / `create_job` when the user did not paste a script **and** did not give a voiceover or talking-head file.

## Auth

```bash
npm i -g @cliptude/cli
cliptude auth login
```

Or `export CLIPTUDE_API_KEY='clp_…'` from /developers/. Never commit keys.

## Commands

```bash
cliptude templates
cliptude estimate --template "Finance vector weekly" --script-file script.txt
cliptude generate --template "Finance vector weekly" --title "Why index funds win" --script-file script.txt --duration 3-4
cliptude generate --template "Finance vector weekly" --title "Why index funds win" --prompt "why most retail traders underperform the S&P over 10 years, keep it for beginners" --duration 3-4
cliptude generate --template "Finance vector weekly" --title "Why index funds win" --voiceover narration.mp3
cliptude generate --template "My talking head" --title "Weekly recap" --talking-head clip.mp4
cliptude generate --template "My avatar weekly" --title "Grandma egg trick" --script-file script.txt --avatar-ai-footage --avatar-intro-only
cliptude script --template "Finance vector weekly" --title "Why index funds win" --prompt "why most retail traders underperform the S&P" --duration 3-4
cliptude voiceover --template "Finance vector weekly" --title "Why index funds win" --script-file script.txt
cliptude continue <job-id>
cliptude status <job-id>
cliptude jobs
cliptude account
```

`generate` returns immediately (`queued`). Poll `status` until `completed` or `failed`. Jobs take 10–40 minutes. Do not block waiting for the MP4.

If the user asked **only for a script** or **only for narration audio**, use `cliptude script` / MCP `create_script` or `cliptude voiceover` / MCP `create_voiceover`. Do not call `create_job`. Poll `get_job` until `completed`, then read `script` or `voiceover.url`. If they then want the MP4, call `cliptude continue` / MCP `continue_job` on that job id (`can_continue` is true). Do not start a second job.

If `templates` is empty, or none fits the video, create one: `get_template_options` (CLI `template-options`) for the format's fields and defaults, `list_voices` (CLI `voices`) for a voice, then `create_template` (CLI `template-create`) with the user's preferences. Send the user to the wizard only if they want to pick the look themselves.

Thumbnails: without a thumbnail setting, each video picks a YouTube style reference for its own title. To set the channel's look, put `thumbnail: {reference_url}` (a YouTube video link or image) or `thumbnail: {custom_prompt}` (people, style, branding; never one video's subject or text) in `create_template` settings (CLI `--thumbnail-reference` / `--thumbnail-prompt`). For one video's own thumbnail idea, pass `thumbnail_prompt` (or `thumbnail_reference_url`) on `create_job` / `create_plan_job` (CLI `--thumbnail-prompt` / `--thumbnail-reference` on `generate` and `plan-job`).

Custom script formatting: spoken words only (no Scene 1, no [Music plays]). See https://cliptude.com/docs/custom-script/

Optional `--duration` (`3-4`, `6-8`, `10-12`, …) overrides the template. Without it, prompt jobs use the template duration and script jobs estimate from word count. `--voiceover` and `--talking-head` ignore `--duration` (length comes from the file; an upload under 6 minutes is refused, like a script under 880 words). MCP: `create_job(..., voiceover_path="/abs/path/narration.mp3")` or `talking_head_path="/abs/path/clip.mp4"` — local stdio only; remote hosts should use the CLI.

Before a long or costly job, or when the user asks what it will cost, call `estimate_credits` (CLI `estimate`) with the same template and prompt/script (an upload as `voiceover_seconds`). It uses the same pricing as `create_job`, creates nothing and returns `credits_required`, `credits_available` and `enough_credits`. An uploaded voiceover bills at the lowest voice rate.

402 = not enough credits (nothing queued). 403 = need a paid plan (SaaS).

Model tier (`generation_model`): `high` is **Cinder**, still pictures and motion graphics only, no video clips; `pro` is **Caldera**, which adds sourced video clips. Use `pro` whenever the video should have moving footage.

Vector Explainer can carry a recurring character. `list_vector_characters` (CLI `vector-characters`) returns the built-in cast (Nova, Kai, Mira, …, with preview images) and the user's own uploads. Put an id in `create_template` settings as `vector_character_id`, or pass `vector_character_id` on `create_job` / `create_plan_job` (CLI `--vector-character`) for one video.

Motion: `vector_reveal_mode` sets how the drawings move. `"none"` (default) keeps each drawing still and moves the camera across it (Ken Burns push, pan, tilt); `"video"` turns every picture beat into a short AI clip and costs more. Set it in `create_template` settings, or per video on `create_job` / `create_plan_job` / `estimate_credits` (CLI `--vector-motion none|video`). Quote the price with `estimate_credits` before switching to video.

To add the user's own character, `upload_vector_character` (CLI `vector-character-upload --name … --file …` or `--url …`) with a picture they gave you, or one you made: one full-body, front-facing character in flat vector style on a plain or transparent background, 1024 px or more, no text. If you made it, show it to the user and upload only after they approve it. The upload returns the id to use; it also appears in the Cliptude wizard. `delete_vector_character` removes one the user no longer wants (refused while a template uses it).

Avatar Video needs an avatar: `list_avatars` (CLI `avatars`, `--section mine` for the user's own) gives ids. Put one in `create_template` settings as `avatar_profile_id` with a voice of the same gender, or pass `avatar_profile_id` (CLI `--avatar`) on `create_job` to use a different avatar for one video.

Avatar Video templates store **Avatar Intro Only** and **AI Image + AI Video**. `list_templates` / `get_template` include `avatar_intro_only` and `avatar_ai_footage` for that format. Override per job with `--avatar-intro-only` / `--no-avatar-intro-only` and `--avatar-ai-footage` / `--no-avatar-ai-footage` (MCP: `avatar_intro_only`, `avatar_ai_footage`). Omit to keep the template. Other formats reject those fields.

## Review, revise and render a finished video

When a job completes you can take the video to final yourself:

1. **Review.** Download `output.url`, sample frames (e.g. `ffmpeg -i video.mp4 -vf fps=1/10,scale=640:-1 frame_%03d.jpg`) and check them against the script: wrong or generic footage, unreadable text, mistimed overlays, music too loud.
2. **Open the timeline.** `cliptude editor <job-id>` (MCP `open_editor_project`) returns the project id and each item as `{id, type, start_s, end_s, text}`. Map every problem to the item ids at that timestamp.
3. **Edit.** One focused fix per run: `cliptude agent <project-id> --prompt "..." --items <ids> --wait` (MCP `run_agent`, then poll `get_agent_run`). One run at a time per project. `failed` or `conflict` → rephrase or retry; do not stack requests.
4. **Check.** Render a draft (`cliptude render <project-id> --wait`, MCP `render_project` + `get_render`) and review it like step 1. Repeat until the video meets the bar the user set.
5. **Finish.** Render the final and give the user `output_url`. Stop at the user's round or credit limit even if minor issues remain, and list them.

Agent runs and renders charge credits.
