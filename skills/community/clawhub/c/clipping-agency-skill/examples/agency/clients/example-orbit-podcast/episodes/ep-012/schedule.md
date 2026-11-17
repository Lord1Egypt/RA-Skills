<!-- written by schedule.py; it replaces this file on every run -->
# Schedule: Example Orbit Podcast, Episode 12: twenty years after the Moon

**EXAMPLE ONLY: a made-up client on NASA footage. The accounts, ids and times are invented; nothing here was posted.**

Times are the client's (America/Chicago). Accounts: TikTok @example.orbit, Instagram Reels @example.orbit, YouTube Shorts @example.orbit

| Clip | Goes out | Where | Approved |
|---|---|---|---|
| 01 | Tue 06 Oct 11:30 America/Chicago (CDT) | TikTok, Instagram Reels, YouTube Shorts | Alex Example (reply, 2026-10-05) |
| 02 | Thu 08 Oct 11:30 America/Chicago (CDT) | TikTok, Instagram Reels, YouTube Shorts | Alex Example (reply, 2026-10-05) |
| 03 | Sat 10 Oct 11:30 America/Chicago (CDT) | TikTok, Instagram Reels, YouTube Shorts | Alex Example (reply, 2026-10-05) |

## Files to upload

Once each, before the requests are written: `media_uploads_create_session` with the client's projectId (example-project-orbit) and the byte size, `upload_parts.py session.json <file>`, `media_uploads_complete_session`. Then save media.json as `{"<file>": {"mediaId": "...", "sha256": "<fingerprint>"}}` and run `schedule.py <batch> --media media.json`.

- `clips/clip-01.mp4` (838506 bytes), fingerprint `28a9ff978696dcbd`
- `clips/clip-02.mp4` (934492 bytes), fingerprint `be95e3bf2c5ede2b`
- `clips/clip-03.mp4` (477203 bytes), fingerprint `c70cd7d8f29fb71c`

## Send

For each request, in this order, one at a time: `schedule.py <batch> --check requests/<name>` (never send a request it refuses), `posts_validate` with the body exactly as written, `posts_create`, then at once `schedule.py <batch> --posted requests/<name> <postId>`.

- `requests/clip-01.json`: clip 01, Tue 06 Oct 11:30 America/Chicago (CDT)
- `requests/clip-02.json`: clip 02, Thu 08 Oct 11:30 America/Chicago (CDT)
- `requests/clip-03.json`: clip 03, Sat 10 Oct 11:30 America/Chicago (CDT)

## Optional, after each Short is live

In YouTube Studio, link the full episode as the Short's related video, if the client wants viewers sent to it (a step in the app).
