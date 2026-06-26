# Operation Patterns - Apple News (MacOS)

Use these patterns to keep behavior deterministic and auditable.

## App Open Pattern

1. Confirm intent to open Apple News app.
2. Launch with `open /System/Applications/News.app`.
3. Verify app state and report success.

## Direct Link Open Pattern

1. Validate link format (`https://apple.news/...`).
2. Preview exact link before launch.
3. Open with `open -a /System/Applications/News.app "<link>"`.
4. Confirm app foreground and link-open outcome.

## Topic Search Pattern

1. Confirm requested topic and scope.
2. If user has a News search shortcut, preview shortcut name and execute.
3. If no shortcut exists, request one reference link or source constraint.
4. Open only approved result links.

## Multi-Link Queue Pattern

1. Present candidate links with index and source.
2. Ask user to select one, or confirm opening multiple.
3. Require second explicit confirmation for more than one open.
4. Report which links were opened.

## Failure Pattern

- If app path launch fails, switch to `osascript activate` fallback.
- If link does not open as expected, retry once with osascript open-location fallback.
- If no safe path exists, stop and provide one actionable fix.
