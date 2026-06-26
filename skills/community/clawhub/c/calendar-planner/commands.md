# CLI Adapter Recipes

Use these recipes when the user wants real calendar actions through a terminal. Show the command first, explain the side effects, and ask before any write.

## Google Calendar via `gcalcli`

```bash
gcalcli --client-id="$GOOGLE_CLIENT_ID" init
gcalcli list
gcalcli --calendar "primary" agenda 2026-03-09 2026-03-16
gcalcli --calendar "primary" search "dentist"
gcalcli --calendar "primary" quick "2026-03-12 09:00 Deep work block"
gcalcli --calendar "primary" import invite.ics
```

Use Google reads to inspect agenda, recent changes, or search results before proposing moves.

## Outlook and Microsoft 365 via Microsoft Graph PowerShell

```powershell
Import-Module Microsoft.Graph.Calendar
Connect-MgGraph -Scopes "Calendars.Read","Calendars.ReadWrite"
Get-MgUserCalendarView -UserId $userId -StartDateTime "2026-03-09T00:00:00+01:00" -EndDateTime "2026-03-16T00:00:00+01:00"
New-MgUserEvent -UserId $userId -Subject "Weekly review" -Start @{DateTime="2026-03-14T17:00:00";TimeZone="Europe/Madrid"} -End @{DateTime="2026-03-14T17:45:00";TimeZone="Europe/Madrid"}
```

Prefer delegated scopes and the smallest time window that answers the question.

## Apple Calendar on macOS via `osascript`

List upcoming events from a named calendar:

```bash
osascript <<'APPLESCRIPT'
tell application "Calendar"
  tell calendar "Work"
    set upcomingEvents to every event whose start date >= (current date)
    repeat with e in upcomingEvents
      log ((summary of e) & " | " & ((start date of e) as text) & " | " & ((end date of e) as text))
    end repeat
  end tell
end tell
APPLESCRIPT
```

Create an event only after approval:

```bash
osascript <<'APPLESCRIPT'
tell application "Calendar"
  tell calendar "Personal"
    make new event with properties {summary:"Gym", start date:date "Thursday, March 12, 2026 at 18:00:00", end date:date "Thursday, March 12, 2026 at 19:00:00"}
  end tell
end tell
APPLESCRIPT
```

## CalDAV and iCloud style stacks via `vdirsyncer` plus `khal`

```bash
vdirsyncer discover
vdirsyncer sync
khal list today 14d
khal calendar
khal new 2026-03-13 08:30 09:00 "School call"
```

Use `vdirsyncer` for sync and `khal` for local read or write after the user confirms the target calendar.

## Normalized review workflow

The local scripts expect one or more JSON files in a simple normalized shape:

```json
[
  {
    "title": "Team sync",
    "calendar": "Work",
    "source": "google",
    "start": "2026-03-10T09:00:00+01:00",
    "end": "2026-03-10T09:30:00+01:00",
    "hard": true,
    "tags": ["meeting"]
  }
]
```

Then run:

```bash
python3 calendar_merge.py work.json family.json > merged.json
python3 calendar_guard.py merged.json
python3 week_plan.py merged.json --start 2026-03-09
```

Use these scripts to defend buffers, spot overload, and generate a weekly repair summary before touching live calendars.
