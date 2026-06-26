---
name: feishu-meeting
description: >
  Create Feishu (Lark) video meetings via Calendar API — instant, scheduled, or recurring.
  Supports multiple invitees (resolved from mobile/email), automatic Feishu VC link generation,
  RRULE-based recurrence, and calendar integration (events appear in attendees' calendars).
  Use when user asks to: create/schedule a meeting, set up a recurring meeting, book a video call,
  开会, 预约会议, 发起会议, 创建周期性会议, 飞书会议.
---

# Feishu Meeting

Create Feishu video meetings with one command. Meetings appear in attendees' calendars with auto-generated VC links.

## Prerequisites

Feishu app permissions (enable in Feishu Open Platform console):
- `calendar:calendar` — Read/write calendars
- `vc:reserve` — Reserve meetings
- `contact:user.id:readonly` — Resolve mobile/email to user IDs

The app must have [bot capability](https://open.feishu.cn/document/uAjLw4CM/ugTN1YjL4UTN24CO1UjN/trouble-shooting/how-to-enable-bot-ability) enabled.

## Configuration

Before first use, set these values in `scripts/create.sh`:
- `DEFAULT_OWNER_OPEN_ID` — Open ID of the default meeting owner (required)
- `CALENDAR_ID` — The bot's primary calendar ID (run the discovery command below)

### Discover Calendar ID

```bash
# After configuring Feishu appId/appSecret in openclaw.json:
curl -s "https://open.feishu.cn/open-apis/calendar/v4/calendars" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import json,sys
for c in json.load(sys.stdin)['data']['calendar_list']:
    print(f\"{c['calendar_id']}  {c['type']}  {c['summary']}\")"
```

Use the `primary` calendar ID.

## Usage

```bash
scripts/create.sh "Topic"                                         # Instant (5min from now)
scripts/create.sh "Topic" --start "2026-03-10 14:00" --duration 60  # Scheduled
scripts/create.sh "Topic" --invitee "13800138000"                   # With invitee
scripts/create.sh "Topic" --invitee "a@b.com" --invitee "138..."    # Multiple
scripts/create.sh "Topic" --rrule "FREQ=WEEKLY;BYDAY=WE;COUNT=8"   # Recurring
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--invitee <mobile\|email>` | Add invitee (repeatable) | Owner only |
| `--start <datetime>` | Start time `"YYYY-MM-DD HH:MM"` | Now + 5 min |
| `--duration <min>` | Duration in minutes | 60 |
| `--rrule <rule>` | RFC 5545 recurrence rule | None |

Positional args after topic are treated as invitees for convenience.

### RRULE Examples

| Pattern | RRULE |
|---------|-------|
| Every Monday | `FREQ=WEEKLY;BYDAY=MO;COUNT=52` |
| Every weekday | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=52` |
| Biweekly Wednesday | `FREQ=WEEKLY;INTERVAL=2;BYDAY=WE;COUNT=26` |
| Monthly 1st Friday | `FREQ=MONTHLY;BYDAY=1FR;COUNT=12` |
| Daily for 5 days | `FREQ=DAILY;COUNT=5` |

**Important**: Feishu requires `COUNT` or `UNTIL` in recurrence rules. The script auto-appends `COUNT=52` if neither is present.

## How It Works

1. Gets `tenant_access_token` from Feishu app credentials
2. Creates a calendar event with `vchat.vc_type: "vc"` (auto-generates Feishu VC link)
3. Resolves invitee mobiles/emails → open_ids via `batch_get_id`
4. Adds attendees to the calendar event (they see it in their Feishu calendar)

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `99991672` | Missing permission | Enable the required scope in app console |
| `190002 invalid parameters` | Bad RRULE or timestamp | Ensure RRULE has COUNT/UNTIL; timestamps are Unix seconds |
| Invitee not found | User not in app's visibility scope | Add user to app's contact scope, or share link manually |
| `121003 param error` on reserves API | Wrong field in payload | Don't pass `invitees` to `/vc/v1/reserves/apply` — it doesn't exist |
