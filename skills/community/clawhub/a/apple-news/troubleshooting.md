# Troubleshooting - Apple News (MacOS)

## `open -a News` Fails

Symptoms:
- Command cannot find application named `News`.

Actions:
1. Use absolute path launch: `open /System/Applications/News.app`.
2. For link opens, use `open -a /System/Applications/News.app "<url>"`.
3. Re-run command-path probe and store working path.

## Apple News URL Scheme Fails

Symptoms:
- `applenews://` returns no registered application error.

Actions:
1. Use `https://apple.news/...` links instead.
2. Open links through News.app absolute path.
3. Avoid undocumented scheme assumptions.

## AppleScript UI Search Blocked

Symptoms:
- `System Events` reports no permission to send keystrokes.

Actions:
1. Do not rely on UI keystroke automation by default.
2. Use direct Apple News links or a user-owned Shortcut.
3. If user wants UI scripting, explain Accessibility permission requirements first.

## Shortcut Path Fails

Symptoms:
- `shortcuts run` fails or shortcut not found.

Actions:
1. Validate with `shortcuts list`.
2. Use exact shortcut name.
3. Fall back to direct app or direct link opening.

## Link Opens in Wrong Context

Symptoms:
- Link does not open expected article or feed.

Actions:
1. Re-validate link format and source.
2. Retry once with osascript open-location fallback.
3. Ask user for a replacement link if mismatch persists.
