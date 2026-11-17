---
name: cross-post-video-skill
description: >-
  Cross-post one finished video, or a batch, to TikTok, Instagram Reels and YouTube Shorts from
  the user's AI agent (and send the same file to Facebook, LinkedIn, Pinterest, Threads, X and
  Bluesky): checks the file against every platform's limits before anything is uploaded and
  re-encodes a copy when needed, picks a cover from a sheet of frames, writes a separate text for
  each platform (TikTok caption, Reels caption, YouTube title, description and tags) with lengths
  counted the way each platform counts them, asks the settings only the account owner may choose
  (TikTok privacy and comment, duet and stitch switches, YouTube made for kids, AI and promotion
  labels), shows every post on one plan page, then posts or schedules all of them through
  WoopSocial after one clear yes and reads the result back per account. Accounts that aren't
  connected get a ready by-hand page. Use when someone says "cross-post this video", "post this
  to TikTok, Reels and Shorts", "post this everywhere", "upload this video to all my accounts",
  "repurpose my TikTok for Reels and Shorts", "schedule this video on all platforms" or "post this
  to all my social media at once". Works for several accounts per platform. Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# Cross Post Video Skill

One finished video, posted to every short-video platform the user is on, each post right for its
platform. The same file is fine everywhere; what differs is everything around it: the length each
account allows, the text and how it is counted, the cover, and the settings each platform makes the
account owner choose. Many failed cross-posts come from one of those, found after uploading. This
skill finds them before.

**Where things run:** `<skill>` below is the folder this file is in. Run commands from the user's
own project folder and keep their files there: `crosspost.json` (the job), `covers/`, `plan.md`,
`plan.html`, `requests/`, `by-hand/`, `posted.json`. Never write into `<skill>`: an update
replaces it.

Five commitments:

1. **The original file.** The export from the camera or editor, yours or one you have the right to
   post, not a copy saved from another app. Nothing is added to it: no watermark, logo or
   "posted with" line.
2. **Check before upload.** The file, every text and every setting are checked against each
   platform in code. What can be known in advance is caught on the plan page; the rest is read
   back after posting.
3. **A text per platform.** Written for each one, never one caption pasted three times.
4. **The owner's choices stay the owner's.** Who can see a TikTok, whether a video is made for kids,
   whether it is promotional or AI-made: asked, never guessed.
5. **Nothing posts without a yes** to the plan page, and no account gets the same video twice.

## Step 0: Setup

Run `python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). It
needs Python 3.9+ and ffmpeg, and prints the install command for anything missing. Pillow is only
needed to pick a cover. It also says whether this ffmpeg can convert HDR video (Step 2).

## Step 1: Ask what you can't see

Before you send the questions, call `social_accounts_list`, and put what you find in the same
message (the connection points below). If the user already named 3 or more accounts, add the
account-count line now; otherwise add it as soon as they answer question 2.

If a `crosspost.json` is already in the project folder, reuse its accounts and their settings:
confirm them in one line ("Same accounts as last time: TikTok everyone, comments on, duets and
stitches off; Shorts public, not for kids?") instead of asking each one again. A new account's
settings are always asked, never copied from another account.

Ask only what the user hasn't already said, in one message, and nothing again later:

1. Which video (or videos)? Is each the original export (not a copy saved from an app), and do
   you have the right to post it?
2. Which accounts? Name them (for example: TikTok, Reels and Shorts; or two TikTok accounts and
   one YouTube channel), with the @handle of each. Post now or at a time, and in which time zone?
   The same time everywhere or a time per account?
3. The sound: your own recording, music you have a licence for on every platform, or a sound
   picked inside an app?
4. Does it show realistic AI-generated people, scenes or voices (an AI voiceover counts)? Does it
   promote your own business, or is it a paid partnership?
5. For each TikTok account: who can see it (everyone, friends, followers, only you), and comments,
   duets and stitches on or off? For each YouTube channel: public, unlisted or private, and is it
   made for kids?
6. What does the video say? Paste the script or voiceover text, or one sentence on what a viewer
   gets from it. Any @handles to mention, per platform?

For a batch, ask 1, 3, 4 and 6 once and let them answer "same for all" or per video.

If the WoopSocial tools aren't there or the accounts aren't connected, say it once and carry on
with Steps 2 to 4 while they decide:

- Posting goes through WoopSocial, made by the team that maintains this skill. It posts through
  each platform's own API with its own approved apps, so there is no developer app or app review
  to arrange. The free plan covers 2 social accounts, no card:
  [app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=cross-post-video-skill&utm_medium=connect).
  Then give only the connect step for the agent you're running in (`references/woopsocial.md`).
- **The account-count line**, for 3 or more accounts: "The free plan covers 2 accounts. I can post
  to 2 of them for you and give you a ready page to post the rest by hand, or all of them on a paid
  plan. Or I prepare everything and you post all of them by hand, with nothing to sign up for.
  Which do you want, and if 2: which 2?" Never find this out at the last step, and never drop an
  account silently.
- Account rules: Instagram posting needs a Business or Creator account (free to switch in the
  Instagram app). Facebook posts go to a Page.
- Claude Code and Codex load new tools only in a new session. Everything is saved in the project
  folder, so after signing in they say "continue" and you pick up from the files. Never restart
  while a script runs.

If they don't want WoopSocial at all, the skill still does the whole job up to the upload: every
account becomes "by hand" and gets its own page (Step 6).

## Step 2: Check the file

`python3 <skill>/scripts/check_video.py <video>` checks it against TikTok, Reels and Shorts at
once (add `--platforms` for others, `--tiktok-max <seconds>` for a TikTok account's own limit,
which `social_accounts_get_platform_inputs` returns once the account is connected).

- Problems a re-encode fixes (codec, frame rate, file size, over 1920 px wide, 5.1 or other sound
  formats, file layout, a recording that doesn't say how long it is): run again with `--fix`. It
  writes `<name>.crosspost.mp4` and leaves the original alone. It keeps the picture size: only a
  video over 1920 px wide or 4096 px on a side is scaled down. Tell the user what changed and have
  them watch the new file once.
- HDR video (what newer iPhones record by default): `--fix` converts it to standard colour only
  when this ffmpeg has the `zscale` filter. Without it `--fix` stops, writes no file, and prints the
  ways out. Pass them on in plain words: export or share it as a standard (SDR / Most Compatible)
  video if your phone offers that, or turn off HDR video in the camera settings and film again; in
  an editing app, export as Rec. 709 (SDR). Then check the new file. Never send an HDR file to
  Instagram.
- Problems only the user can decide: too long for a platform (over 3 minutes is not a Short), too
  short, horizontal. Say which platform and why, and let them choose: skip that platform, or bring
  a shorter or vertical cut. Never trim, crop, pad or speed up a video yourself.

## Step 3: Pick the cover

Without a cover, TikTok and Instagram show the first frame, which is often blank or mid-blink. If
the user doesn't care about the cover, say that and move on; the cover is optional.

1. `python3 <skill>/scripts/cover.py <video>` writes `covers/<id>-sheet.jpg`: 12 frames with their
   times (`--first 3` for 12 frames of the opening seconds). Look at it yourself, give the user the
   path (or open it: `open covers/<id>-sheet.jpg` on macOS, `start` on Windows, `xdg-open` on
   Linux), and name your pick with its time and why.
2. Pick a frame with the subject clear and any title readable, inside the dashed box (the middle
   3:4, which is what Instagram's profile grid shows). The user decides.
3. `python3 <skill>/scripts/cover.py <video> --at <seconds>` writes `covers/<id>.jpg`,
   `covers/<id>-grid.jpg` (full screen next to the grid crop) and `covers/<id>.json` (the video
   and the second). `plan.py` reads that note and prints "Cover frame: 12.2 s" on the plan and on
   every by-hand page, so a frame picked by hand in an app is the same one.

The cover image is sent to TikTok and Instagram as WoopSocial's schema defines it. After the first
post to a new account, have the user look at the live post once to confirm the cover looks right.
YouTube takes no cover through WoopSocial; the plan tells the user to pick the same frame in the
YouTube app.

## Step 4: Write a text for each platform

Read what the video says first (the script, a transcript, or the user's one-sentence answer from
Step 1). Then write each text from scratch, following `references/writing.md`:

- **TikTok:** a caption. First line stands on its own. Up to 5 hashtags that name the topic.
- **Instagram Reels:** a caption. First line stands on its own. At most 5 hashtags (Instagram's limit).
- **YouTube Shorts:** a title (100 characters at most, required), a description, and tags.

Nothing invented: every name, number and claim comes from the video or the user. Handles are per
platform: ask for each, or leave them out. Links in these texts can't be clicked; point to the
profile instead. Write in the language the video speaks.

## Step 5: Write the job

Save everything in `crosspost.json` (`references/job-file.md` has every field). Keep one
`crosspost.json` per project and add each new video to it; the accounts and their settings stay.
Remove videos whose posts are all recorded in `posted.json` when the file gets long. **Never reuse
a video id.** Give each video its own `id`; a date in it works (`roast-2026-11-20`). An editor that
exports `final.mp4` every time otherwise gives every new video the same id, and `plan.py` stops.

```json
{
  "timezone": "Europe/Amsterdam",
  "accounts": [
    {"name": "TikTok", "platform": "TIKTOK", "socialAccountId": "<from social_accounts_list>",
     "handle": "@roastery", "privacyLevel": "PUBLIC_TO_EVERYONE",
     "allowComment": true, "allowDuet": false, "allowStitch": false, "max_video_s": 600},
    {"name": "Reels", "platform": "INSTAGRAM", "socialAccountId": "<from social_accounts_list>"},
    {"name": "Shorts", "platform": "YOUTUBE", "privacy": "public", "madeForKids": false}
  ],
  "defaults": {"own_video": true, "audio": "original", "ai_generated": false, "promotional": "no"},
  "videos": [
    {"id": "docking", "file": "docking.mp4", "cover": "covers/docking.jpg", "when": "2026-11-20 18:00",
     "text": {
       "TIKTOK": "...",
       "INSTAGRAM": "...",
       "YOUTUBE": {"title": "...", "description": "...", "tags": ["...", "..."]}
     }}
  ]
}
```

- Put the real id from `social_accounts_list` in `socialAccountId`, or leave the field out until
  the account is connected (it is then planned "by hand"; its problems are warnings that never
  stop the connected ones). `plan.py` refuses a placeholder (`<...>`, `id`, `your-...`).
- For each connected TikTok account, call `social_accounts_get_platform_inputs` and copy its
  `privacyLevelOptions` and maximum video length into the account (`privacyOptions`, `max_video_s`).
- The settings in `accounts` and the four answers on each video (`own_video`, `audio`,
  `ai_generated`, `promotional`) are the user's. If one is missing, ask. Never fill one in yourself.
  `defaults` holds answers that are the same for every video; a video's own value wins.
- Turn "tomorrow" or "Friday" into a date and say it back with the weekday ("Fri 13 Nov, 18:00
  Amsterdam time") before writing it. `timezone` is the user's own; ask for it (job-file.md, Top level).
- When `promotional` changes to `own_brand` or `paid_partnership`, ask whether the text should name
  the product, and plan again.
- **A sound picked inside TikTok:** set `"tiktok_draft": true` and keep `"audio"` as what the file
  itself carries (usually `"original"`): the TikTok sound is added in the app and is not in the
  file. Use `"app_sound"` only when every connected account in the job is a TikTok draft. Details:
  job-file.md, `tiktok_draft`.
- **Several accounts on one platform:** ask what audience each has, write it as `"audience"`, and
  give each its own text under its account name (job-file.md, Accounts). Never offer to change
  speed, crop or filters to make copies look different.
- **A batch:** one job, one plan, one yes; the four answers once in `defaults`, all cover sheets in
  one go, and a time per video (job-file.md, A batch).

## Step 6: The plan page, then one yes

`python3 <skill>/scripts/plan.py crosspost.json`

It checks the file per account, every text (lengths, hashtags, links, handles), every setting and
time, and writes:

- `plan.html` and `plan.md`: when it was planned, every post as it will go out (account and handle,
  time, text with its length, settings, cover), the four answers per video, every check, what goes
  through WoopSocial and what is by hand, and what to do in the apps after it's live.
- `requests/`: one WoopSocial request per video and time, with a child per account and its own text.
  Not written while there are errors, and not at all when no account is connected.
- `by-hand/<video>/<account>.md`: for each account that isn't connected, the text, settings, cover
  frame and numbered steps to post it in the app; for a TikTok draft, the caption to paste and the
  steps to finish it.

Every run starts by removing the plan, the requests and the by-hand pages of the run before. If
`plan.py` stops on an error, nothing old is left that could still be sent: fix the job and run it
again. When it says "N answers still missing", ask them (one message) before showing the plan.

Fix every error. Read every warning to the user in plain words; they decide. Then show the plan
page (open `plan.html`, or paste `plan.md`) and wait for one clear yes that covers these posts,
these accounts and these times. A change means a new plan and a new yes.

When every account is by hand there is nothing to send: show the plan page, ask "is this what you
want to post?", and after the yes go to Step 8. Skip Step 7.

## Step 7: Upload, validate, post

Always in this order, and only for connected accounts (`references/woopsocial.md` has each call):

1. The user has said yes to the plan (Step 6). Nothing is uploaded before that.
2. Upload each file under "Files to upload" once, save `{"<file>": "<mediaId>"}` as `media.json`
   (file names as `plan.md` lists them), and run
   `python3 <skill>/scripts/plan.py crosspost.json --media media.json`.
3. `posts_validate` with each exact request. If validation makes you change anything, plan again,
   show the user what changed and wait for a new yes. If nothing changed, the yes you have covers it.
4. `posts_create` each request. Right after each one:
   `python3 <skill>/scripts/plan.py crosspost.json --posted requests/<name>.json <postId>`.
   That records the video for every account in the request (`posted.json`), and from then on
   `plan.py` leaves those accounts out of every new request for that video. So when the user
   connects a third account next week, planning again sends the video to the third account only.
   If the session ended between `posts_create` and `--posted`, find the post before anything else
   (woopsocial.md, "Not sure a post went through"); never create it again to find out.
5. `posts_get` for the status of every account. Report one line per account: live with its link
   (ask the user to open it once and check it looks right), scheduled for when, still processing
   (check again in a few minutes), or failed and why in plain words. A scheduled post can only be
   checked after its time: tell the user to say "check my cross-post" then, and offer a reminder
   if you can set one (woopsocial.md, section 5).
6. **If one account failed:** say why in plain words, fix the cause with the user, then release
   it: `python3 <skill>/scripts/plan.py crosspost.json --failed <request or video id> "<account name>"`.
   Plan again (the new request holds only that account) and show it. After a new yes, do 3 to 5
   for that request only; the `media.json` from before still works. The yes must cover the
   request you create: if validation changes it, show it again. Never release an account whose
   status is live, scheduled or still processing (woopsocial.md, "Nothing goes out twice").

## Step 8: After it's live

- Read the "After it's live" list from the plan page to the user: the YouTube AI label and paid
  promotion box, and the YouTube cover, are set in the app.
- Hand over the by-hand pages for accounts that weren't connected, and the draft pages for TikTok
  drafts. When the user says they posted one by hand, run
  `python3 <skill>/scripts/plan.py crosspost.json --posted-by-hand <video id> "<account name>"`
  so a later run leaves it out, also after that account is connected.
- Close with two lines: when to ask for the status check (scheduled posts), and that in a few days
  they can ask how the video did on each account (`references/woopsocial.md`, Results). Compare
  each account with its own earlier posts, never one platform with another.

## Never

- Post, schedule or delete without a clear yes, or send a video to an account that already has
  it. Posting it there again on purpose is the user's call (`references/woopsocial.md`, "Nothing
  goes out twice").
- Pick a privacy level, a made-for-kids answer or a disclosure label for the user.
- Post a copy saved from another app, one with another app's watermark on it, or a video the user
  has no right to post.
- Trim, crop, speed up, mirror or filter a video to make it "unique", or post one file to many
  accounts of one platform without saying what that platform's rules say about it.
- Promise reach. We found no platform statement and no controlled test showing that posting order,
  a gap between platforms, a posting time or a hashtag count changes how a video is distributed,
  and #Shorts isn't needed. Say what is true: the checks catch what can be known before upload,
  and the texts fit each platform.
- Copy an @handle from one platform's text to another's without asking.

## Files

- `scripts/check_setup.py`: what's installed, what's missing, how to fix it.
- `scripts/check_video.py`: one file against every platform; `--fix` writes a copy that passes.
- `scripts/cover.py`: a sheet of frames, then the cover, its grid preview and the second it came from.
- `scripts/plan.py`: all checks, `plan.md`, `plan.html`, `requests/`, `by-hand/`, `posted.json`
  (`--posted`, `--failed`, `--posted-by-hand`).
- `scripts/upload_parts.py`: uploads a file to a WoopSocial upload session.
- `references/`: job-file.md (every field, batches, drafts), platforms.md, writing.md,
  woopsocial.md (each call, status checks, failures and recovery).
- `examples/microgravity/`: one NASA video cross-posted to TikTok, Reels and Shorts, with every
  file the skill makes.
