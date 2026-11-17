---
name: calendar-subscribe
version: 1.0.0
description: >
  Turn a school or work timetable (xlsx / csv) into a shareable HTTPS ICS
  subscription. Split class blocks into sessions, add one travel alarm per day
  (first class only), host a WeChat/iOS/Android landing page. Use when the user
  says 课表订阅, 日历订阅, timetable to ICS, calendar subscription, 同步到日历,
  webcal, 开学课表, share calendar with classmates. NOT FOR one-off local Calendar.app
  AppleScript dumps, Google Calendar API event-by-event writes, or todo/reminder apps.
metadata:
  openclaw:
    emoji: "📅"
    requires:
      anyBins: ["python3"]
    os: ["darwin", "linux"]
---

# Calendar Subscribe

Turn a timetable file into a **subscription calendar** (one HTTPS `.ics` + a tiny landing page). Classmates add it once; you update the file when the schedule changes.

## When this skill is on

User wants classmates / family to **subscribe**, not import a one-shot dump. Typical: school timetable, weekend MBA grid, recurring office hours.

## Workflow

1. **Parse** the source (xlsx grid or csv event list). Skip holiday / "no class" cells.
2. **Split** each teaching block into the actual session times (do not merge a whole morning into one 3-hour event unless the user asks).
3. **ICS** with a real timezone (`TZID`, not floating local), CRLF, UTF-8 line fold on character boundaries.
4. **Travel alarm once per calendar day**, on the earliest class only. Default offset 90 minutes. Later sessions that day get no commute alarm.
5. **Host** the `.ics` on any public HTTPS static path. `Content-Type: text/calendar`.
6. **Landing page** that branches: WeChat → "open in browser"; iOS → `webcal://`; Android → Google Calendar `cid=` + raw ICS.
7. **Verify** in the same turn: `curl -sI` both `/path` and `/path/`; count `BEGIN:VEVENT` and `BEGIN:VALARM`; `VALARM` count must equal distinct class days.

## Source formats

### A. Event list CSV (preferred when you can export it)

```
date,start,end,title,location,notes
2026-09-12,09:00,10:30,Finance,Room 222,week 1
```

### B. Chinese-university weekend grid xlsx

- Row of week labels, row of Excel serial dates, row of 周六/周日
- Time-slot rows (morning / afternoon / evening)
- Merged holiday cells: read the merge origin; if text matches skip patterns, emit nothing

Default skip regex: `不上课|放假|补班`

If the sheet only lists two clock ranges per period (e.g. 09:00–10:30 and 10:45–12:15), emit **two** events, not four 45-minute 节.

## ICS rules

- `METHOD:PUBLISH`, `X-WR-CALNAME`, `X-WR-TIMEZONE`, `REFRESH-INTERVAL;VALUE=DURATION:P1D`
- `DTSTART` / `DTEND` with `TZID=<IANA>` (default `Asia/Shanghai`)
- Stable `UID` from date+start+title so republishing does not duplicate on clients that key on UID
- Fold lines at ≤73 UTF-8 bytes **on codepoint boundaries** (do not split a Chinese character)
- Escape `\`, `;`, `,`, newlines
- `VALARM` `TRIGGER:-PT{N}M` only on the day's first event

Use `scripts/build_ics.py`. Example:

```bash
python3 scripts/build_ics.py \
  --xlsx timetable.xlsx \
  --out timetable.ics \
  --name "Fall timetable" \
  --location "Room 222" \
  --tz Asia/Shanghai \
  --travel-minutes 90
```

CSV path: `--csv events.csv` instead of `--xlsx`.

## Hosting

Any HTTPS static file is enough. Apple Calendar, Google Calendar, and most Android calendars fetch from **their** servers, so the URL must be reachable from the public internet, not only the author's LAN.

Minimum nginx (adapt root and URL prefix):

```nginx
location = /cal {
    return 301 /cal/;
}
location ^~ /cal/ {
    alias /var/www/cal/;
    index index.html;
    types {
        text/calendar ics;
        text/html html;
        image/jpeg jpg jpeg;
        image/png png;
    }
    add_header Cache-Control "public, max-age=3600";
}
```

Landing template: `references/landing.html`. Replace `ICS_URL` and `PAGE_URL`.

Poster / QR: generate a **real** QR of `PAGE_URL` (script or `qrcode` lib). Never let an image model draw the code. Leave a square hole on the poster and composite.

## Verify (same turn, or do not claim it works)

```bash
curl -sI https://example.com/cal      # must 301 → /cal/
curl -sI https://example.com/cal/     # text/html 200
curl -sI https://example.com/cal/timetable.ics   # text/calendar
```

Count:

- `BEGIN:VEVENT` = number of real sessions (not holidays)
- `BEGIN:VALARM` = number of distinct class days
- zero holiday phrases in summaries

## Gotchas

- **`/cal` without a trailing slash is not `/cal/`.** A prefix location `^~ /cal/` misses `/cal`. On a SPA host the bare path falls through to `index.html`. If that app sends `Cross-Origin-Embedder-Policy: require-corp`, the page looks "broken" or blank. Always add `location = /cal { return 301 /cal/; }`.
- **Do not write nginx backups into `sites-enabled/`.** A `.bak` is loaded as a second server; duplicate `listen 443` fails `nginx -t`.
- **Port 80 `return 404` (leftover certbot) makes http links look dead.** 301 to https.
- **A location that sets any `add_header` drops parent `add_header`s.** COOP/COEP on the server block will not apply — usually what you want for a calendar page.
- **WeChat in-app browser cannot add calendars.** Detect `MicroMessenger` and tell the user to open in the system browser first.
- **Google Calendar mobile app cannot subscribe from a URL.** The `https://calendar.google.com/calendar/r?cid=` link works in a browser; OEM calendars can open the raw `.ics` as a one-shot import (no later refresh).
- **Commute alarm is per day, not per session.** 09:00 class → 07:30 leave. Do not also alarm 10:45 / afternoon / evening.
- **UTF-8 fold:** taking `bytes[:73]` can land inside a 3-byte Chinese character and crash encode. Fold on characters, measuring encoded length.
- **Excel dates** are serials from 1899-12-30 when `data_only=True`.
- **Image-model QR codes do not scan.**
- **Domestic clients vs a US VPS:** the author's phone may not reach the host. Give the raw ICS URL as a fallback; Google/Apple fetchers are usually outside the same firewall.

## Examples

```
User: 把这张课表做成可以分享的日历订阅
→ parse xlsx → ICS → host → landing → verify VEVENT/VALARM
```

```
User: 通勤提前一个半小时，别每节课都响
→ --travel-minutes 90, first class of each day only
```
