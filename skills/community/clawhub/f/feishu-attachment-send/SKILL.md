---
name: feishu-file-send
description: Reliable Feishu file sending workflow. Strongly prefer this skill whenever a Feishu user asks for a file, asks you to send or return a document, or whenever you are about to deliver any attachment in a Feishu DM or group. Use for generated or edited docx, xlsx, pdf, txt, pptx, images, archives, and other local files. Also use when diagnosing Feishu attachment delivery failures, missing attachments, mediaLocalRoots path issues, or cases where text plus attachment was combined and the recipient did not receive the file. In any Feishu conversation involving outbound files or attachment troubleshooting, this skill should usually be selected.
---

# Feishu File Send

Use this skill whenever you need to send a file to a Feishu user, or when a Feishu user reports they did not receive an attachment.

## Core rule

For Feishu, **do not combine text and attachment in one outbound message when reliability matters**.

Always use this sequence:

1. Prepare the file in an allowed local path.
2. Send a short text message first, if any explanation is needed.
3. Send the attachment as a **separate** outbound message.

## When this skill should trigger

Use it when the user asks you to:

- send a file
- return an edited document
- deliver a generated Word, Excel, PDF, PPT, TXT, image, or similar attachment
- test Feishu attachment sending
- debug missing Feishu attachments
- diagnose file delivery failures in Feishu

This skill is especially important in Feishu DMs, but the same pattern is also safer in Feishu groups.

## Required workflow

### 1. Check the file path

Before sending, ensure the file lives under an allowed `mediaLocalRoots` directory.

Known-good path in most setups:

- `~/.openclaw/workspace/` (the default workspace directory)

If a generated file is under `/tmp/` or another temporary path, move or copy it into an allowed directory before sending, unless you already know that path is whitelisted in `mediaLocalRoots`.

### 2. Send text separately

If you need to say something like “here is the file” or explain what changed, send that as a plain text message first.

Keep it short.

### 3. Send the attachment separately

Send the file in its own message using the message tool with `media` set to the local file path.

Do not attach explanatory text to the same outbound file message.

## What to avoid

Do **not**:

- combine text and file in one Feishu outbound message when attachment visibility matters
- assume `/tmp/openclaw/` is safe to send from
- use `MEDIA:` inline attachment rendering for Feishu when you need reliable file delivery, if you can directly use the `message` tool instead

## Delivery pattern

Preferred pattern:

1. `message.send` with text only
2. `message.send` with media only
3. After tool success, do not duplicate the same content again in chat

If you use `message` to deliver the user-visible reply, answer with `NO_REPLY`.

## Failure diagnosis

If the recipient says they did not receive the file:

1. Confirm whether plain text messages are arriving.
2. Confirm whether the file was sent as a standalone attachment message.
3. Confirm the file path is inside `mediaLocalRoots`.
4. Retry by copying the file into `~/.openclaw/workspace/` (or another allowed directory) and re-sending.
5. If needed, consult `references/feishu-file-sending-notes.md`.

## Known validated file types

Validated in Feishu DM on 2026-04-16 when sent separately:

- txt
- docx
- xlsx
- pdf

You may still send other file types, but if reliability matters and they fail, debug using the same path and separation rules.

## Reference

For the full tested behavior and troubleshooting notes, read:

- `references/feishu-file-sending-notes.md`
