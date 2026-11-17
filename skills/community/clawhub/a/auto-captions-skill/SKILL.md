---
name: auto-captions-skill
description: >-
  Auto captions for videos, made on the user's own computer by their AI agent: transcribes speech
  with a time for every word (free local Whisper by default, or the user's own Groq or Deepgram
  key, or existing subtitles), proofreads names and numbers, burns creator-style captions into the
  video (8 presets: word highlight, bold, pill, reveal, two-line, clean subtitles, minimal, one
  word) in any shape (9:16, 4:5, 1:1, 16:9, crop or blurred background), writes SRT, VTT and a
  transcript, translates the captions into other languages with the same timing, shows a review
  sheet with each app's buttons drawn on, and posts or schedules the captioned videos to TikTok,
  Reels, Shorts, LinkedIn, Facebook, X, Threads and Bluesky through WoopSocial after a yes. Use when
  someone says "auto captions", "add captions", "add subtitles to my video", "caption generator",
  "subtitle generator", "burn in subtitles", "TikTok captions", "make an SRT", "translate my
  subtitles" or "caption this folder of videos". No watermark, no per-minute limits, no paid API
  needed. Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# Auto Captions Skill

Many people watch with the sound off; captions let them follow along. Good captions are accurate (names and numbers
right), short enough to read at a glance, timed to the speech, placed clear of each app's buttons,
and in a style that fits the account. Accessible captions also need a subtitle file and a
transcript, because burned-in text can't be resized or read aloud.

This skill does all of it on the user's own computer, with no watermark and no per-minute limit.
You (the agent) do the part tools get wrong: you proofread the transcript, choose what to stress,
and translate.

**Where things run:** `<skill>` below is the folder this file is in. Run commands from the user's
own project folder and keep their files there: the job file, `work/` (transcripts, fixes) and
`captioned/` (results). Never write into `<skill>`: an update replaces it.

Five commitments:

1. **Their words, spelled right.** Every transcript is proofread before anything is burned in:
   names, brands, numbers and jargon. Nothing is reworded beyond what was said.
2. **Readable first.** Short chunks at a size people can read on a phone, never ending on "the",
   never splitting "9 or 10 minutes", and kept clear of each app's buttons.
3. **Look before rendering.** A review sheet first; the user approves the look and the text.
4. **Always a subtitle file.** SRT, VTT and a transcript with every video, for accessibility and
   for platforms that take a subtitle file.
5. **Nothing posts without a yes.** Posting is optional and comes last.

## Step 0: Setup

Run `python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). It
needs Python 3.9+, Pillow and ffmpeg, plus one transcription route; it prints the install command
for anything missing. The free route is `pip install faster-whisper` (runs locally; the model
downloads once, about 0.5 GB for "small"). On Apple Silicon, `pip install mlx-whisper` is faster.
A Groq key (`GROQ_API_KEY`, about $0.04 per hour of audio) or a Deepgram key (`DEEPGRAM_API_KEY`,
labels speakers) is quicker for long videos; the audio is then sent to that service, so ask first.

## Step 1: Ask what they need

In one message, ask only what you can't see:

1. Which videos (a file, several, a folder)?
2. Where are they going, and on which accounts? This sets the shape: one 9:16 version fits TikTok,
   Reels and Shorts alike; LinkedIn and X take 1:1, 4:5 or 16:9; YouTube long videos keep 16:9 and
   are better with a subtitle file than burned-in captions. Save the places in `post_to` (for
   example `["TIKTOK", "INSTAGRAM", "YOUTUBE"]`). If they name places to post, also ask: "Should I
   post or schedule them there when they're done, or just hand you the files?" A yes is a request
   to post (below). "Just the files" means no posting talk until the end.
3. Names, brands and terms that must be spelled right (these go in `vocab`).
4. A look: offer to show the styles on their own video (Step 4) instead of describing them. Brand
   colour, if they have one.
5. Other languages, if they reach people in more than one. Each language usually goes to its own
   account (a Spanish TikTok next to the English one), since one account posting the same video
   twice looks like reposting.

Save the answers in `captions.json` (the job file):

```json
{
  "videos": [{"file": "clips/launch.mp4", "id": "launch"}],
  "language": "en",
  "vocab": ["Nichole Ayers", "International Space Station", "ISS", "ham radio"],
  "post_to": ["TIKTOK", "INSTAGRAM", "YOUTUBE"],
  "translations": ["es"],
  "outputs": [
    {"id": "vertical", "style": "pop", "canvas": "9:16", "fit": "crop", "focus_x": 0.55},
    {"id": "linkedin", "style": "clean", "canvas": "4:5", "fit": "blur", "languages": ["en"]}
  ]
}
```

Every field is described in `references/job-file.md`. A folder of videos is just a longer
`videos` list; every script skips work that is already done, so a batch can stop and resume.

**If the user asked to post** (in their request or their answers; naming an app only sets the
shape and is not a request to post): check `social_accounts_list` now, not at the end. If
WoopSocial isn't connected, say it in one short message and carry on with the captions while they
set it up:

- Posting goes through WoopSocial, made by the team that maintains this skill. The free plan
  covers 2 social accounts, no card. They can make the account now, while the videos are being
  captioned: [app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=auto-captions-skill&utm_medium=connect).
  Then give only the connect step for the agent you're running in (`references/woopsocial.md`).
- Claude Code and Codex load new tools only in a new session, and a restart stops a running
  script. Never add the connection or restart while a script runs (transcription or render). The best moment is the review
  pause in Step 5: everything is saved in the project folder and every script resumes, so after
  signing in they say "continue" and you pick up from the files.
- Say the account rules now, so nobody finds out at the last step: Instagram posting needs a
  Business or Creator account (free to switch in the Instagram app), and TikTok asks who can see
  each post.

At Step 6, check `social_accounts_list` again instead of repeating this.

## Step 2: Transcribe

`python3 <skill>/scripts/transcribe.py captions.json`

It picks the best route available (the video's own .srt/.vtt next to it, a Groq or Deepgram key,
mlx-whisper, then faster-whisper) and writes `work/<id>/transcript.txt` (numbered lines) and
`transcript.json` (every word with its time). `--model turbo` is more accurate and slower; use it
for hard audio, accents or many names. Music-heavy or singing videos transcribe poorly: if the
user has a clean voice track, caption from that.

## Step 3: Proofread (never skip)

1. `python3 <skill>/scripts/fix.py captions.json --report` lists unsure words, near-misses of the
   vocab names and split numbers.
2. Read every line of `work/<id>/transcript.txt`. Fix misheard words, names, numbers (write them
   as digits: "17,500"), and missing punctuation, which decides where captions break.
3. Write `work/<id>/fixes.json` (`references/proofreading.md`): corrected lines, whole-word
   replacements, and `emphasis`, the 1 or 2 words per sentence that carry the point (numbers,
   names, the payoff); styles colour them. Fillers (um, uh) are removed unless the user wants them.
4. Ask the user only about what you can't know (how to spell a person's name, a product term).

Don't change what someone said to make it sound better. Captions transcribe; they don't edit.

## Step 4: Subtitles, translations and the look

1. `python3 <skill>/scripts/captions.py captions.json` writes `captioned/<id>/<id>.<lang>.srt`,
   `.vtt` and `.txt` (subtitle cues follow broadcast rules: 2 lines of 42 characters at most,
   broken at punctuation).
2. Translations: fill each `work/<id>/translate.<lang>.json` (`references/translation.md`): every
   cue's meaning in natural language, about as long as the original, names and numbers kept.
   Then run `captions.py` again. Timing comes from the original, so it stays in sync.
3. `python3 <skill>/scripts/styles.py captions.json --at <a second with speech>` puts every style
   on one frame of their video (`captioned/styles-<id>.jpg`). Show it; let them pick. Styles are
   in `references/styles.md`; a brand colour goes in `style_overrides`.

## Step 5: Review, then render

1. `python3 <skill>/scripts/render.py captions.json --preview` writes
   `captioned/<id>/review-<id>.jpg`: three moments per output and language, and for 9:16 the same
   frame with TikTok's, Reels' and Shorts' buttons drawn on. Check that captions don't cover a
   face, existing on-screen text (a name title, a slide) or the buttons; move them with
   `"position"` (0.05 top to 0.95 bottom) per output or per video, and the crop with `focus_x`.
2. Show the sheet and the transcript. Wait for a yes on the look and the words.
3. `python3 <skill>/scripts/render.py captions.json` renders every video, output and language
   to `captioned/<id>/<id>.<output>.<lang>.mp4` (H.264, AAC, ready to post) with a cover frame,
   and lists them in `captioned/manifest.json`. Expect one to three times the video's length in
   render time per output, depending on the computer.
4. Hand over: the videos, the SRT/VTT for each, and the transcript. For a batch, add: every script
   skips finished work, so next week they can drop new videos in the same folder and say "caption
   the new ones".

## Step 6: Post texts, a schedule, and posting

After delivering, offer once, in one line, using the places from `post_to` (skip this if they
chose "just the files" in Step 1). For example: "Want post
texts and a schedule for these too? One a day on TikTok, Reels and Shorts from tomorrow. I can
schedule them for you, or you post by hand from the plan." If not, stop here.

On a yes:

1. Write `post.json` (`references/posting.md`) from what you already know: one account per place
   and language from Step 1, the post text per video and language, the times they gave (or the
   defaults, said as defaults), starting tomorrow. Leave out `socialAccountId` for accounts that
   aren't connected yet. The post text is what search reads: say what the video is about in plain
   words, 3 to 5 specific hashtags at most. TikTok's privacy level and YouTube's "made for kids"
   are the user's answers; ask, never pick them.
2. `python3 <skill>/scripts/post_plan.py post.json` checks every file against each platform
   (length, size, frame rate, shape, text limits), plans one post a day per account at most, and
   writes `plan.md` and `requests/captions/`. It works without WoopSocial. Show `plan.md`: it has
   every file, text and time, and where to add each subtitle file, so they can post by hand from it.
3. To schedule it for them: posting goes through WoopSocial, made by the team that maintains this
   skill; one connection covers TikTok, Instagram, YouTube, Facebook, LinkedIn, X, Threads and
   Bluesky through each platform's own API, with no developer app of their own. The free plan
   covers 2 social accounts, no card. If the plan uses more than 2 accounts, say so plainly before
   connecting and let them choose which to start with; the others stay in the plan. Check
   `social_accounts_list`; connect what's missing in one pass (`references/woopsocial.md`), then
   run `post_plan.py` again with the IDs.
4. Upload each file once (`references/woopsocial.md`), save `media.json`
   (`{"captioned/x/x.vertical.en.mp4": "<mediaId>"}`), run `post_plan.py post.json --media media.json`.
5. `posts_validate` each request, show `plan.md`, and wait for one clear yes for the batch. Then
   `posts_create` each, and report what was scheduled and anything that failed, in plain words.
6. WoopSocial posts the video; it doesn't attach subtitle files. `plan.md` lists where to add
   each SRT (YouTube Studio, Facebook) after the post is live. X and LinkedIn take a subtitle file
   only while uploading in their own app, so there the burned-in captions do the job.
7. Close with one line: they can ask you in a week how the videos did, and you'll read the numbers
   back (`references/woopsocial.md`, Results).

## Never

- Burn in a transcript nobody read. A misspelled name burned into a video can't be fixed after posting.
- Claim captions boost reach or SEO. Say what's true: they let people follow with the sound off, and
  the post text (not the captions) is what search reads.
- Caption someone else's video for reposting, or add a watermark, logo or "made with" line.
- Translate in a way that changes the meaning, or caption music lyrics the user has no right to.
- Post, schedule or delete without a clear yes.

## Files

- `scripts/check_setup.py`: what's installed, what's missing, how to fix it.
- `scripts/transcribe.py`: words with times (faster-whisper, mlx-whisper, Groq, Deepgram, existing subtitles).
- `scripts/fix.py`: proofreading report; applies `fixes.json` with word times kept.
- `scripts/captions.py`: SRT, VTT, transcript; translation templates.
- `scripts/styles.py`: every style on a frame of the user's video.
- `scripts/render.py`: review sheet; burns captions in each output, shape and language.
- `scripts/post_plan.py`: platform checks, schedule, WoopSocial requests, `plan.md`.
- `scripts/upload_parts.py`: uploads a file to a WoopSocial upload session.
- `styles/*.json`: the 8 presets. `fonts/`: Poppins, Anton, Inter (SIL Open Font License).
- `references/`: job-file.md, proofreading.md, translation.md, styles.md, platforms.md, posting.md, woopsocial.md.
- `examples/iss-radio/`: two NASA clips captioned in English and Spanish, with every file the skill makes.
