# ClawHub Publisher Checklist

## Before publish
- Confirm the skill folder path.
- Confirm `SKILL.md` frontmatter is valid.
- Confirm local packaging succeeds.
- Confirm version intent with the user.
- Confirm warnings have been reviewed, not ignored.

## After publish
- Confirm `clawhub inspect` shows the expected latest version.
- Confirm the expected version is visible in recent versions.
- Check the web page if scan or UI state matters.
- Distinguish between:
  - publish failure
  - latest/tag mismatch
  - pending scan
  - suspicious scan from real metadata/code mismatch

## Practical heuristics
- Many rapid versions usually mean the process is broken, not just evolving.
- Validation errors outrank memory of the docs.
- Scan mismatches usually come from declaration drift, not random platform bugs.
- Never tell the user a command worked without checking the output.
