# The client file: clients/<client-id>/client.json

One file per client, written by `client.py new` and checked by `client.py check`. Every script reads
it: the brand for the clips, the names and no-go topics for the checks, the approvers and the
approval rule for the page, the cadence and time zone for the schedule, the accounts for posting,
the agreed numbers for the report. Paths (logo, font) are from the client's folder.

```json
{
 "id": "example-orbit-podcast",
 "name": "Example Orbit Podcast",
 "status": "active",
 "example": false,
 "show": "Example Orbit Podcast",
 "sources": [{"type": "rss", "url": "https://example.com/feed.xml"}],
 "platforms": ["TIKTOK", "INSTAGRAM", "YOUTUBE"],
 "clips_per_episode": 3,
 "agreed_clips_per_month": 6,
 "cadence": {"days": ["tue", "thu", "sat"], "times": ["11:30"], "max_per_day": 1,
             "min_gap_hours": 3, "start_after_hours": 2},
 "timezone": "America/Chicago",
 "brand": {"accent": "#FFD60A", "text": "#FFFFFF", "hook_bg": "#FFD60A", "hook_text": "#0B132B",
           "uppercase": true, "font": null, "logo": "brand/logo.png", "logo_position": "top-left",
           "logo_scale": 0.16,
           "end_card": {"text": "Full episode: Example Orbit Podcast", "seconds": 1.5,
                        "bg": "#0B132B", "color": "#FFD60A"}},
 "names": {"Apollo": ["Appolo"], "Moonwalk": ["moon walk"]},
 "no_go": ["budget cuts", "politics"],
 "approvers": [{"name": "Alex Example", "contact": "alex@example.com"}],
 "approval": {"rule": "hold"},
 "guest_release": "per_episode",
 "youtube": {"privacy": "public", "madeForKids": false},
 "woopsocial": {"projectId": "<from projects_create>", "accounts": {
   "TIKTOK": {"socialAccountId": "<id>", "handle": "@show", "status": "CONNECTED",
              "privacyOptions": ["PUBLIC_TO_EVERYONE", "SELF_ONLY"], "max_video_s": 600},
   "INSTAGRAM": {"socialAccountId": "<id>", "handle": "@show", "status": "CONNECTED"},
   "YOUTUBE": {"socialAccountId": "<id>", "handle": "@show", "status": "CONNECTED"}}},
 "agency": {"name": "Your agency", "reply_to": "clips@your-agency.example"},
 "report": {"recipients": ["alex@example.com"]},
 "expect_episode_every_days": 7
}
```

| Field | What it is |
|---|---|
| `id` | the folder name: lowercase letters, digits, single dashes |
| `name`, `show` | as the approval page and the report show them |
| `status` | `active`, `paused`, `offboarding`, `offboarded` (offboarding is set by `client.py offboard`) |
| `example` | `true` only for made-up demo clients: "EXAMPLE ONLY" on every clip, page and report |
| `sources` | `{"type": "rss", "url"}` (a podcast feed; `"backfill": true` to queue older episodes too) or `{"type": "folder", "path"}` (a local or synced folder). Empty when the client sends files. |
| `platforms` | TIKTOK, INSTAGRAM, YOUTUBE: the client's own accounts the clips go to |
| `clips_per_episode` | as agreed, 1 to 12; the batch may hold fewer when the episode has fewer strong moments |
| `agreed_clips_per_month` | the number the report compares delivery against |
| `cadence.days`, `cadence.times` | posting days (`mon` to `sun`) and clock times in the client's time zone |
| `cadence.max_per_day` | posts a day on this client's accounts, at most TikTok's daily cap (15) |
| `cadence.min_gap_hours` | never two of this client's posts closer than this (default 3) |
| `cadence.start_after_hours` | the earliest slot is this long after scheduling: 1 to 168 hours (default 2). Never under an hour, so there is always time to cancel a post if the client changes their mind; `schedule.py --check` also refuses to send a request less than 30 minutes before its time |
| `timezone` | an IANA name like `America/Chicago`; posting times are the client's, daylight saving included |
| `brand` | caption accent and text colours, the hook box colours, uppercase captions, a `.ttf`/`.otf` font (else Poppins), a logo (PNG with transparency is best) and its corner, and an optional end card (0.5 to 3 s, or `null` for none) |
| `brand.end_card` | optional. It names the show at the end, but it adds seconds that viewers may swipe away on, and it stops a clip from looping cleanly into its start. Many clients go without; agree it with them |
| `names` | `{"Right Spelling": ["wrong one", ...]}`: applied to every caption word on the clip, and any wrong spelling in a hook, title or caption is an error |
| `no_go` | words or topics the client never wants clipped: an error unless the clip only mentions it in passing and `no_go_reviewed` in the batch says why (the client sees that note) |
| `approvers` | who may approve: `{"name", "contact"}`. A reply from anyone else is refused |
| `approval.rule` | `hold` (default: silence means nothing posts) or `auto_after_hours` with `hours` (1 to 336) and `agreed_in_writing` (where and when the client agreed, like "email from Sam, 2 Nov 2026"). Auto-approval never covers a clip the client marked change or skip, and never chooses TikTok's settings: without the client's choice TikTok waits |
| `guest_release` | `per_episode` (each batch says whether its guests' releases are on file) or `covered_by_contract` with `guest_release_note` naming the clause |
| `youtube` | `privacy` (public, unlisted, private) and `madeForKids`: the channel owner's answers, never guessed |
| `woopsocial` | the client's own project and accounts, filled in by `client.py project` and `client.py accounts`. An account whose `status` isn't `CONNECTED` (it needs a new link) is never posted to: the schedule lists it under "By hand" until the client connects it again |
| `agency` | the agency name and reply address the page's "email it" link uses |
| `expect_episode_every_days` | `status.py` says an episode is late after this many days |

`client.py check` errors stop clips, pages and posts for that client until they are fixed.
