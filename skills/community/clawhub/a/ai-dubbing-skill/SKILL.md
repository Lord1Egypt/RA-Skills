---
name: ai-dubbing-skill
description: >-
  AI dubbing for videos, made on the user's own computer by their AI agent: transcribes the speech,
  proofreads it, translates it for the ear and the clock, speaks it in another language with a free
  local voice (Kokoro or Piper: Spanish, Portuguese, French, Italian, German, Dutch, Polish, Hindi
  and more) or the user's own ElevenLabs key (any language, or their own cloned voice), fits every
  line into the time the speaker took, mixes it over the original sound, burns in captions in the
  new language, and posts each language to its own TikTok, Reels or Shorts account through
  WoopSocial after a yes, with the AI-voice label on. Use when someone says "AI dubbing", "dub my
  video", "dub this into Spanish", "translate my video with voice", "video translator", "voice over
  in another language", "multilingual channel", "reach Spanish or Brazilian viewers" or "post my
  videos in other languages". No paid API needed. Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# AI Dubbing Skill

A dub lets people who don't speak the speaker's language hear the video in their own. A good dub
says the same thing in natural words, starts each line when the speaker starts it, finishes in
about the same time, keeps the music and sound underneath, and goes to an account that posts in
that language. A dubbed video is labelled as having an AI voice; that's honest, and the apps ask
for it.

This skill does all of it on the user's own computer. You (the agent) do the part tools get wrong:
you proofread the transcript, translate it for speaking, shorten lines that run long, and pick the
voice with the user.

**Where things run:** `<skill>` below is the folder this file is in. Run commands from the user's
own project folder and keep their files there: the job file `dub.json`, `work/` (transcripts,
translations, voices) and `dubbed/` (results). Never write into `<skill>`: an update replaces it.

Five commitments:

1. **Their meaning, in natural speech.** The transcript is proofread first; the translation keeps
   every point, names and numbers, in words a native speaker would say.
2. **In time with the speaker.** Every line starts where the speaker started it and fits the time
   they took. Lines that don't fit are shortened by you, not rushed past 1.15x or cut off.
3. **Listen before rendering.** The user hears the dub and sees the review sheet before the videos
   are made.
4. **Honest about the voice.** The voice is labelled as AI on every post. A cloned voice is only
   ever the user's own, or one they have the speaker's written consent for. No lip sync is
   claimed: the mouth doesn't move to the new words.
5. **Nothing posts without a yes.**

## Step 0: Setup

Run `python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). It
needs Python 3.9+, Pillow, numpy and ffmpeg, one transcription route, and one voice route; it
prints the install command for anything missing. The free set is
`pip install pillow numpy faster-whisper kokoro-onnx soundfile`, plus `pip install piper-tts` for
German, Dutch, Polish, Russian and the other Piper languages (`references/voices.md`). Models
download once to the user's cache folder (about 0.5 GB for transcription, 120 MB for Kokoro).

## Step 1: Ask what they need

In one message, ask only what you can't see:

1. Which videos (a file, several, a folder)? They must be the user's own or ones they have the
   rights to dub and post. A dub of someone else's video is a copy of it.
2. Which languages, and where each goes. Each language usually gets its own account (a Spanish
   TikTok next to the English one): the same video twice on one account looks like reposting. Save
   the places in `post_to` (`["TIKTOK", "INSTAGRAM", "YOUTUBE"]`). If they name places to post, also
   ask: "Should I post or schedule them there when they're done, or just hand you the files?" A
   yes is a request to post (below).
3. The voice: offer to play samples of the free voices on their own video (Step 5) instead of
   describing them. If they want their own voice, or a language the free voices don't speak, that
   is their own ElevenLabs key (`references/voices.md`); the text goes to ElevenLabs and uses their
   credits.
4. Names, brands and terms that must be spelled and said right (`vocab`).
5. The shape: one 9:16 version fits TikTok, Reels and Shorts; YouTube long videos keep 16:9.

Save the answers in `dub.json` (the job file, `references/job-file.md`):

```json
{
  "videos": [{"file": "clips/names.mp4", "id": "names"}],
  "language": "en",
  "vocab": ["Bob Behnken", "Dragon", "SpaceX"],
  "translations": ["es", "pt-BR"],
  "voices": {"es": "kokoro:em_alex", "pt-BR": "kokoro:pm_alex"},
  "dub": {"background": "voiceover"},
  "post_to": ["TIKTOK", "INSTAGRAM", "YOUTUBE"],
  "outputs": [{"id": "vertical", "style": "pop", "canvas": "9:16", "fit": "crop",
               "languages": ["es", "pt-BR"], "style_overrides": {"max_width": 0.72}}]
}
```

A folder of videos is just a longer `videos` list; every script skips work that is already done,
so a batch can stop and resume.

**If the user asked to post:** check `social_accounts_list` now, not at the end. If WoopSocial
isn't connected, say it in one short message and carry on while they set it up:

- Posting goes through WoopSocial, made by the team that maintains this skill. The free plan
  covers 2 social accounts, no card. They can make the account now, while the videos are being
  dubbed: [app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=ai-dubbing-skill&utm_medium=connect).
  Then give only the connect step for the agent you're running in (`references/woopsocial.md`).
  If the plan has more than 2 accounts (two languages on TikTok and Reels is already 4), say so
  now, plainly.
- Claude Code and Codex load new tools only in a new session, and a restart stops a running
  script. Never add the connection or restart while a script runs. The best moment is the
  listening pause in Step 5: everything is saved in the project folder and every script resumes,
  so after signing in they say "continue" and you pick up from the files.
- Say the account rules now: Instagram posting needs a Business or Creator account (free to switch
  in the Instagram app), and TikTok asks who can see each post.

## Step 2: Transcribe

`python3 <skill>/scripts/transcribe.py dub.json`

It picks the best route available (the video's own .srt/.vtt, a Groq or Deepgram key, mlx-whisper,
then faster-whisper) and writes `work/<id>/transcript.txt` (numbered lines) and `transcript.json`
(every word with its time). `--model turbo` is more accurate and slower; use it for hard audio,
accents or many names.

## Step 3: Proofread (never skip)

1. `python3 <skill>/scripts/fix.py dub.json --report` lists unsure words, near-misses of the vocab
   names and split numbers.
2. Read every line of `work/<id>/transcript.txt`. Fix misheard words, names, numbers and missing
   punctuation, which decides where lines break.
3. Write `work/<id>/fixes.json` (`references/proofreading.md`). Don't reword what was said.
4. Ask the user only what you can't know (how to spell a person's name, a product term).

A wrong word here is spoken wrong in every language.

## Step 4: Translate for the ear and the clock

1. `python3 <skill>/scripts/captions.py dub.json` writes `work/<id>/translate.<lang>.json`, one
   entry per cue.
2. Fill every `text` (`references/translation.md`): the meaning in natural spoken words, about as
   long in time as the original, which usually means fewer words than the source. Names and
   numbers stay.
3. Run `captions.py` again. It writes the subtitle files and warns about cues that read too fast;
   shorten those now.

## Step 5: Voices and the dub

1. If the user hasn't picked a voice: `python3 <skill>/scripts/voices.py sample dub.json <lang>`
   makes each free voice say the first lines (`dubbed/voice-samples/`). Let them listen and pick;
   save it in `voices`.
2. `python3 <skill>/scripts/dub.py dub.json` speaks every line, fits it into the speaker's time
   (a touch slower when there's room, up to 1.15x faster when there isn't) and mixes it over the
   original sound (`dub.background`, `references/job-file.md`). With an ElevenLabs voice it first
   prints the character count and stops: ask, then run with `--confirm-cost`.
3. If lines don't fit, it lists them with how much shorter each must be. Shorten those cues in
   `translate.<lang>.json` (same meaning, fewer words), run `captions.py`, then `dub.py` again.
   Only changed lines are spoken again. Use `--force` only if the user accepts lines that are cut.
4. Ask the user to listen to `work/<id>/dub.<lang>.wav` (the finished soundtrack). Wait for a yes
   on the sound before rendering. If they don't speak the language, say plainly that a native
   speaker should listen before it goes to a large audience.

## Step 6: Review, then render

1. `python3 <skill>/scripts/render.py dub.json --preview` writes `dubbed/<id>/review-<id>.jpg`:
   three moments per output and language, and for 9:16 the same frame with TikTok's, Reels' and
   Shorts' buttons drawn on. Check that captions don't cover a face, on-screen text or the buttons;
   move them with `"position"`, and the crop with `focus_x`. Caption styles are in
   `references/styles.md`; `styles.py dub.json --at <second>` shows them all on one frame.
2. `python3 <skill>/scripts/render.py dub.json` renders every video, output and language to
   `dubbed/<id>/<id>.<output>.<lang>.mp4` (H.264, AAC, the dubbed soundtrack, captions in that
   language) with a cover frame, and lists them in `dubbed/manifest.json`. It refuses a dub that no
   longer matches the translation.
3. Hand over: the videos, the SRT/VTT per language, and the transcript.

## Step 7: Post texts, a schedule, and posting

After delivering, offer once, in one line, using the places from `post_to` (skip it if they chose
"just the files"). On a yes:

1. Write `post.json` (`references/posting.md`): one account per place and language, the post text
   per video and language written natively in that language (not machine-translated from the
   English post), the times they gave or the defaults, said as defaults. TikTok's privacy level and
   YouTube's "made for kids" are the user's answers; ask, never pick.
2. `python3 <skill>/scripts/post_plan.py post.json` checks every file against each platform,
   plans one post a day per account at most, turns the AI-generated label on for TikTok and
   Instagram, and writes `plan.md` and `requests/posts/`. It works without WoopSocial. Show
   `plan.md`; they can post by hand from it.
3. To schedule it for them: posting goes through WoopSocial, made by the team that maintains this
   skill; one connection covers TikTok, Instagram, YouTube, Facebook, LinkedIn, X, Threads and
   Bluesky through each platform's own API, with no developer app of their own. The free plan
   covers 2 social accounts, no card. If the plan uses more, say so before connecting and let them
   choose which to start with. Connect what's missing in one pass (`references/woopsocial.md`),
   then run `post_plan.py` again with the IDs.
4. Upload each file once, save `media.json`, run `post_plan.py post.json --media media.json`.
5. `posts_validate` each request, show `plan.md`, and wait for one clear yes for the batch. Then
   `posts_create` each, and report what was scheduled and anything that failed.
6. `plan.md` lists what WoopSocial can't do: YouTube's "Altered or synthetic content" answer in
   YouTube Studio, and where to add each SRT. Tell the user these steps plainly.
7. Close with one line: they can ask you in a week how each language did, and you'll read the
   numbers back (`references/woopsocial.md`, Results).

## Never

- Dub a video the user doesn't own or have the rights to, or a song's lyrics.
- Clone, imitate or name-drop a voice that isn't the user's own (or a speaker who gave written
  consent). Never present a stock voice as the speaker's real voice.
- Claim lip sync, "undetectable" AI, or that a dub boosts reach. Say what's true: it lets people
  hear the video in their language.
- Turn off the AI-generated label on a dubbed post, or skip YouTube's synthetic-content step.
- Change what someone said to make it sound better, beyond what a natural translation needs.
- Post, schedule or delete without a clear yes.

## Files

- `scripts/check_setup.py`: what's installed, what's missing, how to fix it.
- `scripts/transcribe.py`: words with times (faster-whisper, mlx-whisper, Groq, Deepgram, existing subtitles).
- `scripts/fix.py`: proofreading report; applies `fixes.json` with word times kept.
- `scripts/captions.py`: SRT, VTT, transcript; translation templates.
- `scripts/voices.py`: the voice list, samples, downloads, and speech for every engine.
- `scripts/dub.py`: speaks, fits and mixes each language; lists lines that are too long.
- `scripts/styles.py`: every caption style on a frame of the user's video.
- `scripts/render.py`: review sheet; renders each output and language with the dubbed sound.
- `scripts/post_plan.py`: platform checks, AI labels, schedule, WoopSocial requests, `plan.md`.
- `scripts/upload_parts.py`: uploads a file to a WoopSocial upload session.
- `styles/*.json`: 8 caption presets. `fonts/`: Poppins, Anton, Inter (SIL Open Font License).
- `references/`: job-file.md, proofreading.md, translation.md, voices.md, styles.md, platforms.md, posting.md, woopsocial.md.
- `examples/crew-dragon/`: two NASA clips dubbed into Spanish and Portuguese, with every file the skill makes.
