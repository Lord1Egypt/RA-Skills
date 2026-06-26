---
name: bark
description: Send push notifications to iOS devices via Bark app (https://github.com/Finb/Bark). Use when user asks to push a notification to their iPhone, send a Bark notification, or notify via Bark. Triggered by phrases like "send a Bark notification", "push to iPhone", "bark一下", "notify me".
---

# Bark Skill

Send push notifications to iOS devices via the Bark app. The Bark key is stored in `~/.bark/key`.

## Key Setup

Key file: `~/.bark/key` (plain text, just the key string).

If the file doesn't exist or is empty, ask the user for their Bark key and write it to `~/.bark/key`.

## API Overview

- **Base URL**: `https://api.day.app/`
- **Method**: GET or POST
- **Required**: Bark key (from `~/.bark/key`), body text
- **Optional**: title, subtitle, URL, icon, sound, group, level, etc.

## Quick Send (GET)

Send a simple notification:

```
GET https://api.day.app/{key}/{body}
```

Send with title:

```
GET https://api.day.app/{key}/{title}/{body}
```

Send with title and subtitle:

```
GET https://api.day.app/{key}/{title}/{subtitle}/{body}
```

## POST Request (Recommended for multi-line / special chars)

Use POST + `--data-urlencode` for plain text, newlines, and special characters:

```bash
KEY=$(cat ~/.bark/key)
curl -s -X POST "https://api.day.app/$KEY" \
  -d "title=Notification Title" \
  --data-urlencode "body=First line
Second line
Third line"
```

**Notes**:
- Use `-d "title=..."` and `--data-urlencode "body=..."` to separate title and body
- Newlines in body are literal line breaks (press Enter, not `\n` as a string)
- `--data-urlencode` auto URL-encodes, no manual handling needed for Chinese or special chars
- **Do not** use `-d "body=multiline content"` — newlines won't be preserved in form-data

## Parameters

| Param | Description |
|-------|-------------|
| `title` | Notification title, slightly larger than body |
| `subtitle` | Subtitle |
| `body` | Notification body, use `\n` for line breaks |
| `url` | URL to open when notification is tapped |
| `group` | Message group for grouping notifications |
| `icon` | Push icon (iOS 15+) |
| `sound` | Notification sound, e.g. `alarm`, `birdsong` |
| `level` | `active` (default, lights up screen immediately) / `timeSensitive` (shows during Focus mode) / `passive` (adds to list without lighting screen) |
| `criticalAlert` | `true` to play sound even in Do Not Disturb (use with caution) |

## How to Use

1. Read key from `~/.bark/key`
2. If key file doesn't exist or is empty, ask user for their Bark key and write it to `~/.bark/key`
3. Build the request with the key and user-provided parameters
4. Execute via exec/curl
5. Confirm notification received

## Example

Key stored in `~/.bark/key`: `yourkey`
Title: Meeting Reminder
Body: Team sync at 3pm tomorrow

```
curl -s -X POST "https://api.day.app/yourkey" \
  -d "title=Meeting Reminder" \
  --data-urlencode "body=Team sync at 3pm tomorrow"
```

## Notes

- If user doesn't have a Bark key, tell them to install the Bark app and copy the test URL from the app
- Default public server is `api.day.app`; Bark also supports self-hosted servers
- For critical alerts (`level=critical`), the device will play sound even in Do Not Disturb
- Sound will loop for 30 seconds if `call=1` parameter is used
