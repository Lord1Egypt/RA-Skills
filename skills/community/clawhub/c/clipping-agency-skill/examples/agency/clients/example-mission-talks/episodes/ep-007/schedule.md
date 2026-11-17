<!-- written by schedule.py; it replaces this file on every run -->
# Schedule: Example Mission Talks, Episode 7: two days before launch

**EXAMPLE ONLY: a made-up client on NASA footage. The accounts, ids and times are invented; nothing here was posted.**

Times are the client's (America/New_York). Accounts: TikTok @example.missiontalks, YouTube Shorts @example.missiontalks

| Clip | Goes out | Where | Approved |
|---|---|---|---|
| 01 | Fri 13 Nov 18:00 America/New_York (EST) | TikTok, YouTube Shorts | Jordan Example (reply, 2026-11-09) |
| 02 | Mon 16 Nov 18:00 America/New_York (EST) | TikTok, YouTube Shorts | Jordan Example (reply, 2026-11-09) |
| 03 | Wed 18 Nov 18:00 America/New_York (EST) | TikTok, YouTube Shorts | no reply by the deadline on page 2, as agreed in writing (auto, 2026-11-12) |

## Files to upload

Once each, before the requests are written: `media_uploads_create_session` with the client's projectId (example-project-mission) and the byte size, `upload_parts.py session.json <file>`, `media_uploads_complete_session`. Then save media.json as `{"<file>": {"mediaId": "...", "sha256": "<fingerprint>"}}` and run `schedule.py <batch> --media media.json`.

- `clips/clip-01.mp4` (922025 bytes), fingerprint `8b94bd65abb02fa0`
- `clips/clip-02.mp4` (280840 bytes), fingerprint `db76d964db72a22b`
- `clips/clip-03.mp4` (454031 bytes), fingerprint `3e1c3e9ecd369ef4`

## Send

For each request, in this order, one at a time: `schedule.py <batch> --check requests/<name>` (never send a request it refuses), `posts_validate` with the body exactly as written, `posts_create`, then at once `schedule.py <batch> --posted requests/<name> <postId>`.

- `requests/clip-01.json`: clip 01, Fri 13 Nov 18:00 America/New_York (EST)
- `requests/clip-02.json`: clip 02, Mon 16 Nov 18:00 America/New_York (EST)
- `requests/clip-03.json`: clip 03, Wed 18 Nov 18:00 America/New_York (EST)

## By hand

Not connected through WoopSocial: Instagram Reels. Post the same file and that platform's caption from the approval page at the time above, from the client's account, or ask the client to connect it (client.py connect).

## Optional, after each Short is live

In YouTube Studio, link the full episode as the Short's related video, if the client wants viewers sent to it (a step in the app).
