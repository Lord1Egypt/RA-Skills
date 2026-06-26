# Command Paths - Apple News (MacOS)

Use this order for deterministic command selection.

## Priority Order

1. `open` with absolute app path and optional Apple News URL (primary)
2. `osascript` for app activation and URL opening fallback
3. `shortcuts run` for user-owned search/open automations

## Probe Pattern

Run lightweight checks before first operation:

```bash
command -v open
command -v osascript
command -v shortcuts
test -d /System/Applications/News.app && echo "News.app present"
```

## Validated Launch Pattern

Use absolute path based launches:

```bash
open /System/Applications/News.app
open -a /System/Applications/News.app "https://apple.news/AhCs4Rmk1REaKltNwpS4APQ"
```

## osascript Fallback Pattern

```bash
osascript -e 'tell application "News" to activate'
osascript -e 'tell application "News" to open location "https://apple.news/AhCs4Rmk1REaKltNwpS4APQ"'
```

## Shortcut Fallback Pattern

Use only user-owned shortcuts already present on the machine:

```bash
shortcuts list
shortcuts run "<user-shortcut-name>"
```

## Unsupported Path Notes

- `open -a News` may fail on some systems or locales.
- URL schemes like `applenews://` are not reliably registered.
- Direct AppleScript object model for News is limited; do not assume query APIs.
