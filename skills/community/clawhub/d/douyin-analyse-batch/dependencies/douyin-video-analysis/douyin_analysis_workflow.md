# Douyin Video Analysis Workflow

## Trigger
User sends a Douyin URL and wants content analysis.

## Fixed pipeline

### Step 1: Resolve page
- Open short link or full link in Chrome.
- Capture:
  - canonical video URL
  - title
  - page description
  - creator/account
  - visible chapter points

### Step 2: Get media candidates
- Read browser performance resources.
- Look for:
  - `douyinvod`
  - `media-audio`
  - `media-video`
- Save candidate URLs.

### Step 3: Download audio
- Prefer audio stream over full video.
- If 403 occurs:
  - use browser-derived cookie
  - include referer/origin/user-agent
- Save under `/tmp/douyin_transcribe/`.

### Step 4: Transcribe
- Use local `mlx-whisper` in venv.
- Fast-first strategy:
  - first pass with tiny/small model
  - refine if necessary
- Produce:
  - raw transcript
  - cleaned readable draft

### Step 5: Summarize first
Before critique, always add:
- a concise content summary
- a structured summary of hook / main claim / support / ending
- a "useful information + evidence" section

The "useful information + evidence" section should distinguish:
- actual useful facts/claims
- the evidence offered by the video itself
- your initial confidence level

### Step 6: Analyze
Minimum sections:
- What the video says
- Title/hook strategy
- AI-generated likelihood
- Critical-thinking critique
- What is useful vs misleading

### Step 7: Save
Write two notes:
- transcript note
- analysis note

### Step 7: Reply
Tell the user:
- transcript quality level
- main conclusions
- note paths

## Honesty guardrails
- Metadata != full transcript
- Rough machine transcript != polished verbatim script
- Be explicit about confidence and limitations
