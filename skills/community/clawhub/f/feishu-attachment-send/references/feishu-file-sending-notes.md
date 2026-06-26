# Feishu file sending notes

## Tested behavior

Test date: 2026-04-16

Channel: Feishu DM

Verified working when sent as separate messages:

- plain text message
- txt attachment
- docx attachment
- xlsx attachment
- pdf attachment

## Confirmed root cause

The earlier delivery issue was not a file format problem.

The primary issue was that text and attachment were being combined into one outbound message. In that mode, Feishu did not reliably show the attachment to the recipient.

When the assistant switched to this pattern, delivery worked:

1. send a plain text message
2. send the attachment in a separate message

## Path constraints

Feishu local file sending depends on `mediaLocalRoots`.

A file path must be inside an allowed directory. The default workspace path usually works:

- `~/.openclaw/workspace/`

Temporary paths like these may fail unless explicitly whitelisted:

- `/tmp/openclaw/`
- `/tmp/`

## Recommended operational rule

For any Feishu attachment:

- keep explanatory text separate
- send the file by itself
- prefer workspace-local paths

## If a send fails

Check these in order:

1. Is Feishu plain text working?
2. Was the file sent as a standalone attachment message?
3. Is the file path inside `mediaLocalRoots`?
4. If not, copy the file into the workspace and retry.

## Suggested config direction

If dynamic files are commonly generated under `/tmp/openclaw/`, consider adding `/tmp/openclaw` or `/tmp` to Feishu `mediaLocalRoots` and restart the gateway.
