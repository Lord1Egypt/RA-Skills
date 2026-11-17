# crosspost.json: the job file

One file holds everything: where the video goes, the settings the account owner chose, and the
words for each platform. `plan.py` reads it and checks all of it.

```json
{
  "timezone": "America/New_York",
  "accounts": [
    {"name": "TikTok", "platform": "TIKTOK", "socialAccountId": "<from social_accounts_list>",
     "handle": "@roastery", "audience": "English", "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false,
     "privacyOptions": ["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"], "max_video_s": 600},
    {"name": "Reels", "platform": "INSTAGRAM", "socialAccountId": "<from social_accounts_list>"},
    {"name": "Shorts", "platform": "YOUTUBE", "socialAccountId": "<from social_accounts_list>",
     "privacy": "public", "madeForKids": false, "category": "28"},
    {"name": "TikTok ES", "platform": "TIKTOK", "audience": "Spanish", "privacyLevel": "PUBLIC_TO_EVERYONE",
     "allowComment": true, "allowDuet": false, "allowStitch": false}
  ],
  "defaults": {"own_video": true, "audio": "original", "ai_generated": false, "promotional": "no"},
  "videos": [
    {"id": "docking", "file": "clips/docking.mp4", "cover": "covers/docking.jpg",
     "when": {"default": "2026-11-20 18:00", "Shorts": "2026-11-20 20:00"},
     "text": {
       "TIKTOK": "Caption for TikTok...",
       "TikTok ES": "Texto para la cuenta en español...",
       "INSTAGRAM": "Caption for Reels...",
       "YOUTUBE": {"title": "Title, up to 100 characters", "description": "Description...", "tags": ["nasa", "space station"]}
     }}
  ]
}
```

## Top level

- `timezone`: an IANA name (`Europe/Amsterdam`, `America/New_York`, spelled with those capitals).
  Times in `when` are in this zone. An account can have its own `timezone`. It is required as soon
  as any `when` is a clock time: ask the user for theirs. Without it `plan.py` stops and asks for
  it, and it never assumes UTC. A job that only posts "now" needs none. The plan pages say when
  they were planned in this zone ("Planned Thu 12 Nov 2026, 14:05 CET"), so a page opened again
  later shows what its "(in 3 days)" counts from.
- `accounts`: where videos go. `videos`: what goes there.
- `defaults`: optional values every video inherits: `when`, `own_video`, `audio`, `ai_generated`,
  `promotional`, `tiktok_draft`. A video's own value wins. Any other key is an error. The plan
  still prints the four answers on every video, so the yes covers them.

## Accounts

Every account has a `name` (any label, unique) and a `platform`: `TIKTOK`, `INSTAGRAM`, `YOUTUBE`,
`FACEBOOK`, `LINKEDIN` (profile), `LINKEDIN_PAGES`, `PINTEREST`, `THREADS`, `X`, `BLUESKY`.

`socialAccountId` comes from `social_accounts_list`. Leave it out for an account that isn't
connected: it is planned "by hand" and gets a page in `by-hand/`. A placeholder (anything with `<`
or `>`, `id`, or an id starting with `your-`) is an error: "this is the example's placeholder".

Two optional labels, both free text:

- `handle`: the account's @handle. Printed next to the account name on the plan and the by-hand
  page, so twelve accounts can't be mixed up.
- `audience`: who the account is for ("Dutch", "US", "brand B"). When every account on a platform
  that gets the same video has a different audience, the same-platform warning becomes one note
  for the whole job.

**Several accounts on one platform** (two languages, two regions, two brands): ask the user what
audience each account has, write it in the account (`"audience": "Dutch"`), and give each its own
text with `"text": {"<account name>": ...}`. Otherwise the plan warns once per job, with what that
platform's own rules say about the same video on several accounts, and once more when two or more
of those accounts share the platform's text. Never offer to change speed, crop or filters to make
copies look different.

The rest are the account owner's choices. Before an account is connected a missing one is a
reminder; once it is connected it is an error. Never fill one in for the user. The same goes for
every other check: a problem with a by-hand account is a warning and never stops the connected
accounts.

| Platform | Field | Values |
|---|---|---|
| TikTok | `privacyLevel` | `PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`, `SELF_ONLY` |
| TikTok | `allowComment`, `allowDuet`, `allowStitch` | true or false, each one chosen |
| TikTok | `privacyOptions`, `max_video_s` | copied from `social_accounts_get_platform_inputs`: the audiences this account offers and its own maximum video length |
| YouTube | `privacy` | `public`, `unlisted`, `private` |
| YouTube | `madeForKids` | true or false (a legal declaration) |
| YouTube | `category` | optional, a YouTube category number as text (`"28"` is Science & Technology, `"22"` People & Blogs, `"24"` Entertainment, `"27"` Education); the plan shows the name |
| Instagram | `trial` | optional: `"MANUAL"` or `"SS_PERFORMANCE"` posts a Trial Reel, shown to non-followers first |
| Pinterest | `pinterestBoardId` | the board, from `social_accounts_get_platform_inputs` |

## Videos

- `file`: the video, relative to the job file. `id`: a short name (letters, numbers and dashes, in
  any script, 80 at most); defaults to the file name. It names the request and the by-hand folder,
  and `posted.json` records each post under it. **Never reuse a video id for a different video.**
  Give each video its own id; a date in it works (`roast-2026-11-20`). Without one, an editor that
  exports `final.mp4` every day gives every new video the same id. `posted.json` keeps the sha256
  and size of the file that was posted, so a different file under an id that already went out
  stops the plan: "video id 'final' was already posted from a different file; give this video a new
  id". The same file moved to another folder is fine. A re-encoded copy (`--fix`) is a different
  file: if some accounts already have the video, give the copy a new id and list only the accounts
  still waiting in `accounts`.
- `cover`: optional JPEG made with `cover.py`. Sent to TikTok and Instagram. It must really be a
  JPEG: the file's content is checked, not its name. `cover.py --at` also writes `covers/<id>.json`
  (the video and the second); `plan.py` prints that second ("Cover frame: 12.2 s") on the plan and
  on every by-hand page, and warns when the note names another video.
- `when`: `"now"`, or `"2026-11-20 18:00"` (24-hour), or one per account or platform:
  `{"default": "2026-11-20 18:00", "Shorts": "now"}`. Accounts with the same time go out as one
  request. The keys of such an object are account names, platforms of this job, or `default`. Any
  other key is an error that lists the valid ones, and so is an account left without a time when
  there is no `default`. Nothing falls back to "now".
- `accounts`: optional list of account names, when a video goes to only some of them.
- The four answers, all the user's:
  - `own_video`: true when it is the original export and the user made it or has the right to
    post it (their own, a client's, licensed). false for a copy saved or downloaded from an app or
    from someone else's account; false is an error.
  - `audio`: `"original"` (own voice or recording), `"licensed"` (music licensed for every
    platform it goes to) or `"app_sound"` (a sound picked inside an app; it doesn't travel).
  - `ai_generated`: true when it shows realistic AI-generated people, scenes or voices. Sent as
    the AI flag to TikTok and Instagram, as WoopSocial's schema defines it; for YouTube the plan
    lists the Studio step.
  - `promotional`: `"no"`, `"own_brand"` (TikTok's "Promotional content" label) or
    `"paid_partnership"` (TikTok's "Paid partnership" label; the plan lists the Instagram and
    YouTube steps).
- `tiktok_draft`: optional, true or false; the way to use a sound picked inside TikTok. True
  sends the video to each connected TikTok account as a draft in its TikTok inbox, 2 hours before
  the time (or right after the yes when that is too soon), and the user adds the sound, pastes the
  caption and picks the audience in the app. Keep `audio` as what the file itself carries (usually
  `"original"`): the TikTok sound is added in the app and is not in the file. `audio` is per video,
  not per account, so `"app_sound"` stays an error for every other connected account; use it only
  when every connected account in the job is a TikTok draft. `privacyLevel` isn't needed for an
  account that only gets drafts. The plan writes a page per draft with the caption to paste and
  the steps. At most 5 drafts wait per account per 24 hours.
- `text`: one entry per platform, or per account name when two accounts on a platform need
  different words. The account name wins. Two or more accounts of one platform that have no text
  under their own name share the platform's text, and the plan warns.
  - TikTok, Instagram, Facebook, LinkedIn, Threads, X, Bluesky: a string.
  - YouTube: `{"title", "description", "tags"}`. Pinterest: `{"title", "description", "link"}`.

## A batch

One job file, one plan, one yes for the whole batch. Ask the four answers once ("the same for all
ten, or does one differ?") and put them in `defaults`. Make all cover sheets in one go and show
them together. Give every video its own time (and its own id). The plan then has a schedule table
(video by account), warns when one account gets two posts less than 60 minutes apart, and notes
Instagram's 100 API posts per 24 hours and the 5 TikTok drafts per 24 hours only when the job goes
over them. After a partial failure, `posted.json` already holds what went out: release the failed
accounts (SKILL.md Step 7.6) and plan again; the rest is never sent twice.

## What plan.py checks

- The file, per account: length (TikTok's limit is the account's own), size, frame rate, shape,
  codec, colour, sound, and the file layout Instagram needs.
- Each text: length counted the platform's way (`references/platforms.md`, Text), the YouTube title
  and tags, hashtag limits ("#1" is a number, not a hashtag), hashtags that say nothing, links that
  won't be clickable, an @handle reused across platforms, a first line too long to stand alone, the
  same text on two platforms. The length on the plan page is the number the check used.
- Settings and answers: all present, the TikTok audience is one the account offers, a paid
  partnership isn't "only you".
- Times: in the future, and real (not in the hour the clocks skip in spring). The cover: a real
  JPEG under 8 MB, 9:16.
- The same video going to several accounts on one platform (once per job), and accounts sharing
  the platform's text.
- A batch: a schedule table when there are 2 or more videos; one account getting two posts less
  than 60 minutes apart; more than 100 Instagram posts or more than 5 TikTok drafts on one account
  within 24 hours.
- Answers still missing are counted: "3 posts planned, 3 answers still missing".
- `posted.json`: an account that already has a video is left out of every new request; a record
  that matches no account in the job is a warning; a different file under a posted video id stops
  the plan.

## posted.json: what already went out

`plan.py crosspost.json --posted requests/<name>.json <postId>` writes one entry per video and
account for every account in that request:

```json
{
  "docking|<socialAccountId of TikTok>": {"postId": "<postId>", "video": "docking", "account": "TikTok",
                                           "platform": "TIKTOK", "when": "2026-11-20T17:00:00Z",
                                           "request": "docking.json", "recorded": "2026-11-13T09:12:44Z",
                                           "file": "clips/docking.mp4", "sha256": "<64 hex>", "size": 31457280}
}
```

An account with an entry for a video is never put in a new request for that video. The plan shows
it as "already posted (post <id>)", "scheduled for <time> (post <id>)" while its time is still
ahead, or "sent as a draft (post <id>)" for a TikTok draft. A connected account's entry is keyed on
its `socialAccountId`, so it does not depend on the time, on the account's name or on which other
accounts are in the job, and a recorded post whose time has passed is not an error.

- An account whose post failed: `plan.py crosspost.json --failed <request or video id> "<account
  name>"` removes its entry for that video, and the next plan writes a request for only that
  account. The same command posts a video to an account again on purpose; only when the user asks.
- A post the user made by hand: `plan.py crosspost.json --posted-by-hand <video id> "<account
  name>"` writes `"<video id>|hand:<account name>"` with the account's platform. Until the account
  is connected it is matched by name and platform. The first plan after the account gets a
  `socialAccountId` moves the entry to `"<video id>|<socialAccountId>"` (still `"byHand": true`),
  so from then on renaming the account changes nothing.
- An entry for a video in the job that matches no account (an account renamed before it was
  connected, removed, or connected again under another id) is a warning that names it. If that
  account is in the job under a new name it gets the video a second time, so the warning says to
  give it its old name back, or, if the video was never posted there, to release the entry with
  `--failed <video id> "<old account name>"`.
- A `posted.json` that can't be read is an error. `plan.py` never empties it or replaces it with
  anything but the same records (it rewrites it only to move a by-hand entry to the account's id);
  repair it, or move it away if nothing in it was really posted.

## What a run removes

Every run of `plan.py crosspost.json` first removes `plan.md`, `plan.html`, `requests/*.json` and
the pages in `by-hand/` from the run before, then checks the job. A run that stops on an error
therefore leaves no old request behind. `posted.json`, `media.json`, the videos and the covers are
never removed.
