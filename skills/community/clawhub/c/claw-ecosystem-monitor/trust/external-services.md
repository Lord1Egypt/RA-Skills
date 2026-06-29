# External Services

Status: free public skill.

This skill uses public, unauthenticated metadata sources only.

| Service | Purpose | Data Stored | Credentials |
|---|---|---|---|
| GitHub public API | OpenClaw repository metadata and issue/PR metadata | IDs, titles, labels, timestamps, source URLs | None required |
| npm registry API | OpenClaw package and AI/devtool package metadata | package names, versions, timestamps, weekly download counts, source URLs | None required |
| OpenClaw docs and ClawHub public pages | source availability and robots/status checks | status code, timestamp, hash, canonical URL | None required |

Not used:

- paid APIs,
- private repositories,
- account scraping,
- cookies,
- payment processors,
- KYC providers,
- email inboxes,
- analytics trackers.

Stop conditions:

- HTTP 403,
- HTTP 429,
- robots disallow,
- DMCA or abuse notice,
- platform warning,
- request for authentication or private account access.
