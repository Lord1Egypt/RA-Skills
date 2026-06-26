# Release checklist

Use this before publishing a new version.

## User-facing checklist

- Skill name is `discord-voice-agent`
- Description clearly says what it does and when to use it
- README/demo copy explains the install path in plain language
- Existing Discord installs only need the voice channel id
- Fresh installs clearly require the Discord plugin/integration plus token and channel id
- Default model behavior is explained simply
- One-command smoke path is documented
- Troubleshooting section is short and useful

## Runtime checklist

- `npm run smoke` works
- `npm test` works
- first-run wizard flow is documented
- model settings are documented
- fallback behavior is explained
- status/health behavior is visible

## Before publish

- package the skill
- validate the package
- confirm the public-facing wording feels beginner-friendly
- keep feature promises realistic and testable
