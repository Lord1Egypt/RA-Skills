# Security

## Scope

This skill controls a logged-in Douyin Creator Center browser session through Chrome DevTools Protocol. It can upload and publish content from the user's local machine.

## Permissions

- Reads only the video file path passed with `--file`.
- Connects to a local CDP endpoint, defaulting to `http://127.0.0.1:9222`.
- Uses the logged-in browser session to access `creator.douyin.com`.
- Does not request passwords, cookies, or SMS verification codes.

## Reporting

Before publishing a modified version, inspect `SKILL.md` and `scripts/upload_to_creator.js` line by line. Do not add install hooks, obfuscated commands, remote code download, or credential collection.

