# The clip list (clips.json) and the job (clipjob.json)

Both live in the user's project folder, next to `campaign.json`.

## clips.json: what make_clips.py cuts

```json
{
  "video": "interview.mp4",
  "campaign": "campaign.json",
  "style": {"accent": "#FFD43B", "uppercase": false, "hook": true},
  "clips": [
    {"id": "01", "account": "TikTok", "start": 490.0, "end": 513.4,
     "hook": "Astronauts live Groundhog Day on purpose", "reframe": "auto"},
    {"id": "02", "account": "Reels", "start": 214.6, "end": 236.0,
     "hook": "Save the crew, not the mission", "reframe": "auto"}
  ]
}
```

- `video`: the campaign's footage. With `campaign` set, a file not in `footage.files` is refused.
- `campaign`: the on-screen disclosure and watermark (text or logo) come from it, so no clip can
  leave them out.
- `account`: which account the edit is for. One edit per account.
- `start`, `end`: seconds in the source, from `work/transcript.txt`. `snap` moves small slips to
  sentence edges. `cut` removes ranges inside the clip; `tighten` and `fillers` take out pauses
  and "um".
- `id`: letters, digits, dashes or underscores (it becomes the file name `clip-<id>.mp4`).
- `reframe`: `auto`, `face`, `center`, `fit` or `stack`; `focus_x` (0 to 1) and `zoom` (1 to 2)
  set a crop by hand. Phone footage with a rotation flag is read upright.
- `stack`: for a 16:9 stream with a facecam. The facecam fills the top of the frame and the
  gameplay the rest. Give `"facecam": {"x": 1600, "y": 40, "w": 280, "h": 210}` in pixels of the
  source (read them from a frame; `--preview` draws the boxes) and optionally `"game"` the same way
  (default: the whole frame).
- `punch`: `true` adds a small punch-in at sentence breaks of long stretches (crop and stack
  layouts), so a talking clip doesn't sit still for 20 seconds.
- Never `speed`, `mirror`, `flip` or `filter`: make_clips.py stops on them.

`python3 <skill>/scripts/make_clips.py clips.json --transcript work/transcript.json --out clips`
writes `clips/clip-01.mp4` and on, a first-frame JPEG per clip, `contact-sheet.jpg` and
`manifest.json`. The manifest holds each clip's fingerprint (sha256), the source time ranges it
uses, the hook and what is on screen. `check_clips.py` reads it.

`--preview` saves three frames per clip with the crop drawn on, without rendering. `--width 540`
writes smaller files (drafts, examples); platforms take 1080x1920 best.

## clipjob.json: what goes where

```json
{
  "campaign": "campaign.json",
  "manifest": "clips/manifest.json",
  "timezone": "America/New_York",
  "ai_generated": false,
  "accounts": [
    {"name": "TikTok", "platform": "TIKTOK", "handle": "@example.clipper",
     "socialAccountId": "<from social_accounts_list>",
     "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false},
    {"name": "Reels", "platform": "INSTAGRAM", "handle": "@example.clipper.reels",
     "socialAccountId": "<from social_accounts_list>"},
    {"name": "Shorts", "platform": "YOUTUBE", "handle": "@exampleclipper",
     "privacy": "public", "madeForKids": false, "by_hand": true}
  ],
  "posts": [
    {"id": "groundhog-tiktok", "account": "TikTok", "file": "clips/clip-01.mp4",
     "caption": "#ad ... @example.orbit ... #exampleorbit"},
    {"id": "curse-names-shorts", "account": "Shorts", "file": "clips/clip-03.mp4",
     "title": "His goal: future crews forget his name",
     "caption": "#ad ...", "tags": ["nasa", "crew dragon"]}
  ]
}
```

### Top level

- `campaign`: the campaign file. `manifest`: the manifest(s) of make_clips.py (a path or a list).
- `timezone`: the user's own, for the deadlines on the submission sheet (IANA name, such as
  `America/New_York`). Times are shown with the zone's abbreviation (EST or EDT). A time the user
  types without an offset is read in this zone.
- `ai_generated`: does any clip show realistic AI-made people, scenes or voices? The user's answer;
  a post may override it.

### Accounts

- `name`: unique, used everywhere (`"TikTok"`, `"TikTok 2"`). `platform`: `TIKTOK`, `INSTAGRAM`
  or `YOUTUBE`. `handle`: shown on the plan and the sheet.
- `socialAccountId`: from this session's `social_accounts_list`, never from a saved file. Or
  `"by_hand": true` for an account the user posts in the app (its post gets a `by-hand/` page). One
  of the two is required; both together, or a placeholder (`<...>`, `your-...`), is refused.
- `marketplace_verified`: the user's answer to "is this account connected and verified in the
  marketplace?". `false` blocks its posts; left out, the check asks. `verified_in` (a list of
  marketplace names) answers it for every campaign on those marketplaces.
- `audience`: optional, the account's viewer share per country as the app shows it
  (`{"US": 0.62}`); under the campaign's audience rule it warns before posting.
- Saved choices: `plan.py clipjob.json --remember-accounts` saves each account's platform, handle,
  comment/duet/stitch choices, YouTube visibility, made for kids and audience to
  `~/.ai-clipping/accounts.json`. Never saved: the `socialAccountId`, TikTok's `privacyLevel` and
  the marketplace verification. In the next campaign `check_clips.py` shows a "saved choice" note
  for each account whose platform AND handle match (a name alone never matches); nothing is filled
  in. Show the note to the user and write what they confirm into clipjob.json.
- TikTok: `privacyLevel` (`PUBLIC_TO_EVERYONE`, `MUTUAL_FOLLOW_FRIENDS`, `FOLLOWER_OF_CREATOR`;
  `SELF_ONLY` is refused because a paid partnership can't be private), `allowComment`,
  `allowDuet`, `allowStitch`. The user's choices, asked, never filled in. Copy the account's
  `privacyLevelOptions` from `social_accounts_get_platform_inputs` into `privacyOptions`, and its
  maximum length into `max_video_s`.
- YouTube: `privacy` (`public`, `unlisted`, `private`) and `madeForKids`, the owner's declaration.
- Instagram posting needs a Business or Creator account.

### Posts

One per account and edit.

- `id`: short, unique, never reused (it keys the ledger).
- `account`: an account name. `file`: the clip.
- `caption`: starts with the campaign's disclosure (`#ad`), then what the clip says, then every
  required hashtag, @mention and link. For YouTube it is the description; `title` (100 characters
  at most) and optional `tags` are added.
- `approved`: when the brief asks for the brand's approval. `plan.py` writes `approval/<post>.md`
  to send them; record the answer as `{"by": "<who>", "at": "<date>", "sha256": "<first 12 of the
  fingerprint>"}`, so a file changed after approval is caught. `true` alone gets a warning.
- A clip the user made themselves (not in the manifest) also needs `source`
  (`{"file": "interview.mp4", "ranges": [[490.0, 513.4]]}`, seconds in the source) and `on_screen`
  (`{"disclosure": "Paid partnership with ...", "disclosure_seconds": 4, "watermark": null}`),
  filled in after watching the clip. Never declare a disclosure that isn't in the file.

Two posts for one account go into separate requests (one child per account per request).
