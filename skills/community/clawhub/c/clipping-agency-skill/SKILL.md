---
name: clipping-agency-skill
description: >-
  Clipping agency workflow for agencies on retainer, run from the agency's AI agent: one folder per
  client (sources, platforms, clips per episode, posting days and time zone, brand kit, names
  dictionary, no-go topics, approvers), new episodes from a podcast RSS feed, a synced folder or a
  file, 3 to 12 vertical clips per episode in the client's brand with the reason for each moment,
  checks in code (platform specs, names, no-go topics, sponsor segments that need a paid-partnership
  label, guest releases, possible music, clean cut edges, the same clip never for two clients), one
  phone-friendly approval page per episode the client answers in plain words, recorded against
  exactly the clips that page showed, posting only
  approved clips to the client's own TikTok, Instagram Reels and YouTube Shorts through WoopSocial at
  the client's times, a status board of what waits on whom, a monthly report from real numbers, and
  offboarding. Use when someone says "clipping agency", "I clip podcasts for clients", "set up a new
  client", "clip this episode for <client>", "send the client the clips to approve", "the client
  replied", "schedule the approved clips", "what's waiting", "monthly report for <client>" or
  "offboard <client>". Not for clip-army or marketplace campaigns paid per view: that is
  ai-clipping-skill. Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# Clipping Agency Skill

A clipping agency on retainer turns each client's long episodes into short clips, gets the client's
yes, posts them on the client's own TikTok, Instagram and YouTube accounts at the client's times,
and reports every month. The work that loses clients is rarely the editing: it is a clip posted
before anyone said yes, a guest's name spelled wrong, a sponsor read without a label, one client's
clip on another client's account, a report with numbers nobody can check. This skill makes each of
those a check in code.

**Where things run:** `<skill>` below is the folder this file is in. The agency's own folder (the
one holding `clients/`) is where every command runs; never write into `<skill>`, an update replaces
it. One ledger for every client lives in the user's home folder (`~/.clipping-agency/ledger.json`;
`CLIPPING_AGENCY_HOME` moves the folder, `CLIPPING_AGENCY_LEDGER` or `--ledger` names another file).
It records every clip file handed to a client, every account and every post, which is what lets the
skill refuse a clip already used for another client or an account that belongs to someone else,
whatever folder each client lives in. Because of that, **one person on one computer schedules posts
for the whole agency** (or every machine points `CLIPPING_AGENCY_LEDGER` at one shared ledger file);
others can cut clips and make pages.

```
clients/<client-id>/
  client.json  checklist.md  queue.json  sources-seen.json  brand/  reports/  offboard.md
  episodes/<episode-id>/
    batch.json  work/ (transcript)  clips/ (cut clips, manifest.json)  approval/approve-<episode>.html
    approvals.json  schedule.md  requests/  media.json
```

Six commitments:

1. **Nothing posts without the client's recorded yes for that exact file and caption.** A re-cut
   clip or an edited caption needs a new yes. Silence means hold, unless the client agreed in
   writing to approval after a number of hours.
2. **Each client's accounts only.** One WoopSocial project per client; every request is checked
   against the client's file and the ledger.
3. **One clip, one client.** The same file is never handed to two clients.
4. **The client chooses** who sees their TikTok posts, comments, duets and stitches, YouTube's
   made-for-kids answer. Never defaulted.
5. **Honest labels.** A clip with a sponsor segment goes out labelled as paid. Possible music is
   flagged for a listen; nothing adds music.
6. **Real numbers only.** The report shows what WoopSocial's saved analytics say, with what a view
   means on each platform, and says where numbers are missing. Nothing is estimated.

## Step 0: Setup

`python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). Needs Python
3.9+ and ffmpeg; Pillow to cut clips (`pip install pillow`); for transcription faster-whisper (free,
local), the user's own Groq or OpenAI key, or the captions the client's host already made. On Windows
also `pip install tzdata`: schedules run on each client's own clock.

## Step 1: A new client

`python3 <skill>/scripts/client.py new <client-id> --name "Show Name"` writes
`clients/<client-id>/client.json` to fill in with the agency (`references/client-file.md` has every
field). Ask in one message only what the agency hasn't said:

- the platforms, clips per episode and per month as agreed, posting days and times, the client's
  time zone;
- the brand kit: two or three colours, uppercase captions or not, the logo file and its corner, a
  font file if they have one, and whether they want an end card ("Full episode: <show>"; optional,
  since it adds seconds viewers may swipe away on);
- the names dictionary: the host, recurring guests, sponsors and jargon, spelled right, with the
  wrong spellings transcripts make;
- no-go topics; who approves (name and contact); whether silence ever counts as a yes (only with the
  client's written agreement, stated where and when); guest releases (per episode, or a contract
  clause that covers short clips on social);
- YouTube: public, unlisted or private, and made for kids or not (the channel owner's answer).

`python3 <skill>/scripts/client.py check <client-id>` checks every field and writes `checklist.md`.
Fix every error. Show the checklist.

## Step 2: Connect the client's own accounts

Call `social_accounts_list` first. If WoopSocial isn't connected in this agent, put the signup link
at the top of the message: "Posting goes through WoopSocial, made by the team behind this skill. It
posts through each platform's own approved apps, so the agency needs no developer app or app review.
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=clipping-agency-skill&utm_medium=connect).
The free plan covers 2 social accounts; one client on TikTok, Reels and Shorts is already 3, so
agency use is a paid plan. At the time of writing (2026-11-16), Pro is $19 a month for 20 accounts:
six clients on three platforms." Then the connect step for this agent (`references/woopsocial.md`).

`python3 <skill>/scripts/client.py connect <client-id>` prints the steps:

1. `projects_create` with the client's name: **one project per client**, never shared. Then
   `client.py project <client-id> <projectId>`.
2. `oauth_create_authorization` with that projectId for each platform not connected yet (no
   redirectUrl). Hand the agency the links with the client message the script prints; it tells the
   client the permission screen will ask them to allow WoopSocial, the posting service. The client
   opens each link signed in to their own account and allows access. Never ask for, store or type a
   client's password or code, and never sign in as the client.
3. When the client is done: `social_accounts_list` with the projectId (save as `accounts.json`),
   and for TikTok `social_accounts_get_platform_inputs` (save as `tiktok-inputs.json`). Then
   `client.py accounts <client-id> accounts.json tiktok-inputs.json`. It refuses an account another
   client's file or the ledger already names.

Instagram needs a Business or Creator account (free to switch in the app). Until a platform is
connected, its clips are listed to post by hand.

## Step 3: New episodes

`python3 <skill>/scripts/sources.py check --all` reads every client's sources: a podcast RSS feed
(the episode enclosures; the first look takes only the newest, not the back catalogue) or a local or
synced folder. `sources.py add <client-id> <file or link>` queues one the client sent. A YouTube link
is queued but never downloaded: ask the client for the file (better quality anyway), or download it
only when the client owns it and has given the right. An audio-only episode needs the video from the
client, or audiogram clips made by hand.

`sources.py start <client-id> <queue item> --episode <episode-id> [--download]` writes
`episodes/<episode-id>/batch.json`. Fill in the episode's guests and whether their releases are on
file, sponsor segments (start and end in seconds) and any music you know of
(`references/batch-file.md`).

## Step 4: Pick and cut the clips

1. In the episode folder: `python3 <skill>/scripts/transcribe.py <source> --out work` (or
   `--from captions.srt`). Read `work/transcript.txt` and `work/peaks.txt`.
2. Score moments with `references/clip-rubric.md`. Pick 3 to 12, as agreed; fewer strong clips
   beat padding, and say so to the client. Each clip must stand alone and still be true on the day
   it is posted (no "tomorrow", no figure that will change; the year in the hook for old material,
   and `episode.recorded` set). For each: `why` in one sentence (the client reads it on
   the approval page), a hook (8 words or fewer, true to the clip), each platform's caption, the
   YouTube title. Write them into `batch.json`.
3. `python3 <skill>/scripts/make_clips.py <batch.json> --preview`, look at the crops, then
   `make_clips.py <batch.json>`. Every clip gets the client's caption colours, hook box, logo, end
   card if they have one, and the names dictionary on every caption word. Cuts start after the
   previous word ends and stop before the next one, with short audio fades. Two people talking:
   `"reframe": "split"` with a box per speaker; a camera that cuts between shots: `"shots"` re-aims
   the crop per shot. Never speed, mirror, filter or add music. Look at `clips/contact-sheet.jpg`.

Clips the agency cut in its own editor go in with `"file"` and the source `start` and `end`
(`references/batch-file.md`); every check still runs.

## Step 5: Check

`python3 <skill>/scripts/check_clips.py <batch.json>`

Each clip against each platform (length, size, 9:16, caption limits, Instagram's 5 hashtags, the
YouTube title), the names dictionary, no-go topics (in what is said and written), sponsor segments
(the captions must say it is paid; Instagram's and YouTube's labels are set in the apps), sponsor
reads that weren't marked, guest releases, possible music (caption cues like [MUSIC], marked
stretches, sound with no words: a hint, never a guarantee), the same file twice, and a file another
client already has, or this client already had in another episode. With faster-whisper installed it
also listens to the first and last seconds of each cut clip and warns when a word sounds cut off;
without it, it says so and someone listens to each clip's edges. Fix every error. Read each warning
to the agency in plain words; a possible-music or clean-edges warning means someone listens before
the client sees it.

## Step 6: The approval page

`python3 <skill>/scripts/approve.py <batch.json>` writes `approval/approve-<episode>.html`: a small
page that works with no scripts, opened as an attachment on any phone. "Page N" at the top, then
Clip 1, 2, 3... with a cover picture linked to the clip, why it was picked, each platform's caption
and the YouTube title, the planned time in the client's words and zone ("Planned around Wed 07 Oct,
18:00 New York time (EDT)"), anything to know (a paid label, possible music, the year it was
recorded), TikTok's choices for the client to make, and the reply to copy. How the client gets the
clips: send them with the page (the default links `../clips/`), or `--clips-url <https link>` of a
shared folder holding them (best for phones), or `--embed` for a small batch.

When the client agreed to approval on silence, the page shows the deadline as a date and time in the
client's zone, and the rule is stored with the page: changing the client file later never changes a
page already sent. Make the page on the day you send it. Then `approve.py <batch.json> --sent`.

The client replies in plain words, by email or chat:

```
Page 1, Example Mission Talks ep-007
1 yes, 2 yes
3: change: lead with the TV, it's funnier than the complaint
TikTok: followers, comments on, duets off, stitches on
Name: Jordan Example
```

Save it and run `approve.py <batch.json> --apply reply.txt --received "<when the client sent it>"`.
It reads the page number and one answer per clip, prints each line with what it understood, and
records nothing unless every line reads one way. Safety over convenience: it refuses a line that could
mean two things ("All yes but skip 3", "1: yes but change the caption"), a clip with no answer (unless
you pass `--partial`), a reply to an older page once a newer one was sent, a clip number the page
doesn't have, a clip answered twice, a change with no note, a sender who isn't an approver, and a
reply that changes nothing. When it refuses, ask the client what they meant; never guess. Any reply
to a page, even a refused one, ends approval on silence for that page. Without `--received` (or a
`Date:` line in the saved email) the reply time is recorded as unknown, never as the time you applied
it. A TikTok line counts only with all four answers; otherwise nothing is chosen for the client and
TikTok waits.

**If the client says skip or change for a clip already scheduled**, the output says `CANCEL NOW:
post X`: run `posts_delete` with that postId at once, then `schedule.py <batch.json> --cancelled X`.
Do this before anything else. It works only while the post hasn't started going out. Once a part of it
is live, WoopSocial can't delete it (POST_NOT_DELETABLE): `schedule.py --status` says LIVE, NOT
CANCELLED, and the post is removed in the app on that account. Tell the client the same day.

Make the changes asked for, check again, make a new page (the next page number) and send it; clips
approved before stay approved while they are unchanged. `approve.py --status` shows where each clip
stands. `references/approval.md` has the details.

## Step 7: Schedule on the client's accounts

`python3 <skill>/scripts/schedule.py <batch.json>` lists only clips with a recorded yes for exactly
the file and captions they have now, each at the next free time of the client's cadence in the
client's zone (never closer than the client's minimum gap, at most their posts a day, under TikTok's
daily cap, never sooner than an hour from now, and never on a slot another episode of this client
already has planned), and the files to upload. Show `schedule.md` to the agency. Then, in this order
(`references/woopsocial.md`):

1. Upload each file once into the client's project (`media_uploads_create_session`,
   `upload_parts.py`, `media_uploads_complete_session`); save `media.json`; run
   `schedule.py <batch.json> --media media.json`. One request per clip in `requests/`, with a child
   per connected account of this client. Requests are removed whenever a reply is applied, a new page
   is made, a clip is cut again or the client is offboarded, so nothing written for an old state can
   be sent: run `--media` again then.
2. Right before sending each one: `schedule.py <batch.json> --check requests/clip-NN.json`. It
   checks again, now, the approval, that the client is active, the accounts, every check, that the
   clip isn't already sent, and that the time is at least 30 minutes away. Never send a request it
   refuses.
3. `posts_validate` with each body exactly as written. If anything must change, change the batch or
   client file, never the request.
4. `posts_create`, then at once `schedule.py <batch.json> --posted requests/clip-NN.json <postId>`.
   It runs the same checks. If it refuses and the post was already sent: `posts_delete` at once,
   while every account of the post is still NOT_STARTED.
5. After the post time: `posts_get`, save as `status.json`, `schedule.py <batch.json> --status
   status.json`. A failed account: say why, check `social_account_posts_list` for that account before
   anything is sent again.

After a sponsored clip is live: Instagram's paid partnership label and YouTube's "includes paid
promotion" box are set in the apps (`schedule.md` lists them). Platforms not connected: post the same
file and caption by hand from the client's account at the planned time.

## Step 8: What waits on whom

`python3 <skill>/scripts/status.py` shows every client: new episodes not started, an episode later
than the client's usual rhythm, clips not cut or failing checks, pages not sent, clips waiting for
the client and for how long, changes asked for, approved but not scheduled, scheduled, live, failed.
Each client says whether it waits on the agency or on the client. Offer to run it every morning.

## Step 9: The monthly report

At the start of a month, for the client's project: `social_account_posts_list_analytics` with the
month's publish dates (save it), and `social_accounts_get_analytics` per account for the month
(optional, for the follower change). Then
`python3 <skill>/scripts/report.py <client-id> --month 2026-10 analytics.json [--followers ...]
[--notes notes.md]`.

It refreshes each post's status from the analytics instead of trusting the ledger, and stops when a
post that should be live by now doesn't show (run `posts_get` and `schedule.py --status` for it
first), or when the saved reply holds another client's posts. It writes `reports/<month>.md` and
`.html` for the client (forwardable, light and dark, readable on a phone): clips agreed against
delivered and why any are missing, approval turnaround from when the client actually replied,
clips posted on silence counted apart (never as "approved"), views per platform with what a view
means there and days live per clip, the follower change when WoopSocial returns it, and last month
next to this one. Plus `reports/<month>-agency.md` for the agency only: what to chase. Never send
that one. Never add numbers from elsewhere, never estimate one that is missing, never add platforms'
views together (`references/monthly-report.md`).

## Step 10: Offboarding

`python3 <skill>/scripts/client.py offboard <client-id>` stops new work for the client, removes any
unsent requests, and writes `offboard.md`: each scheduled post to cancel (`posts_delete`, then
`--cancelled <postId>`), each account to remove (`social_accounts_delete`, then `--revoked
<PLATFORM>`), the handover (clip files, a last report, deleting their uploaded media), and a message
telling the client how to remove the app's access on the platforms they had connected. Before
closing: `social_account_posts_list` with the client's projectId and NOT_STARTED must show nothing
(posts made on another computer aren't in the ledger), then `--done --nothing-waiting`. Live posts
stay on the client's accounts; only the client deletes those. `client.py release <socialAccountId>`
frees an offboarded client's account if it is later connected for someone new.

## Never

- Post a clip without the client's recorded yes for that exact file and caption, or treat silence as
  a yes without the client's written agreement.
- Post to another client's account, put two clients in one project, or hand one clip file to two
  clients.
- Ask for, store or use a client's password or login code, sign in as the client, or drive anyone's
  logged-in browser.
- Choose the client's TikTok audience or comment, duet and stitch settings, or YouTube's
  made-for-kids answer.
- Add music, speed up, mirror or filter a clip; post a clip with a sponsor segment without saying
  it is paid.
- Post the agency's own clips to fan pages or the agency's accounts with this skill: clip-army and
  marketplace campaigns are ai-clipping-skill's job.
- Promise views, or put an estimated or rounded-up number in a report.

## Files

- `scripts/check_setup.py`: what's installed and how to add what isn't.
- `scripts/client.py`: new, check, list, connect, project, accounts, offboard, release.
- `scripts/sources.py`: check feeds and folders, add, queue, start an episode.
- `scripts/transcribe.py`: word timestamps (local, Groq, OpenAI or existing captions), loudest
  moments, sound cues.
- `scripts/make_clips.py`: vertical clips in the client's brand; names dictionary; manifest.
- `scripts/check_clips.py`: every clip against the platforms, the client and the other clients.
- `scripts/approve.py`: the approval page, `--sent`, `--apply`, `--status`.
- `scripts/schedule.py`: the schedule, `--media`, `--check`, `--posted`, `--cancelled`, `--status`.
- `scripts/status.py`: what waits on whom, every client.
- `scripts/report.py`: the monthly report.
- `scripts/upload_parts.py`: uploads a clip to a WoopSocial upload session and records its SHA-256.
- `scripts/agencylib.py`: shared helpers, platform limits, the ledger, schedules.
- `references/`: client-file.md, batch-file.md, clip-rubric.md, approval.md, platforms.md,
  woopsocial.md, monthly-report.md.
- `examples/`: two made-up clients on NASA footage with every file the skill makes.
