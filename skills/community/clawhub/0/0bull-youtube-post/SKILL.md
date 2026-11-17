---
name: 0bull-youtube-post
description: Publish a YouTube Short from a real rented iPhone through the 0bull MCP server, with the required title, then follow it to a final status.
homepage: https://docs.0bull.net/mcp/overview
---

# Post a YouTube Short with 0bull

0bull rents real iPhones by the month. A Short is published by driving the YouTube app on
one of those phones, so publishing is asynchronous: you queue a submission and poll it
until it reaches a final status.

## Before you start

The 0bull MCP server must be connected:

```bash
openclaw mcp add 0bull --url https://0bull.net/mcp --transport streamable-http
openclaw mcp login 0bull
```

If `list-accounts-tool` is missing, stop and tell the user to run those two commands.

## Publish a Short

1. **Pick the account.** Call `list-accounts-tool` with `platform: "youtube"` and use the
   account's `id` as `account_id`. A YouTube account carries the Google address it posts
   from (`google_email`), which is how you tell similar channels apart.
2. **Provide the video** through exactly one of:
   - `video_url`: a public https URL the server downloads.
   - `upload_id`: call `create-upload-url-tool` (no parameters), then POST or PUT the raw
     video to the returned `upload_url` within 15 minutes, then pass the `upload_id`.

   Supplying both, or neither, is rejected.
3. **Write the title.** On YouTube the `caption` field is the Short's **title**. It is
   required and capped at 100 characters. Agree it with the user; do not invent one.
   Omitting it is refused, because an untitled Short ends up named after the date it was
   posted.
4. **Queue it.** Call `create-submission-tool` with `platform: "youtube"`, `account_id`, the
   video and the title. Add `draft: true` to leave it as a draft on the phone instead of
   publishing. The call returns the submission immediately in `pending`.
5. **Poll** `get-submission-tool` with the returned `submission_id`, leaving a second or two
   between calls.

## Statuses

| Status | Meaning |
| --- | --- |
| `scheduled` | Queued for a future run. |
| `pending` | Queued, not picked up yet. |
| `ingesting` | The video is being fetched or prepared. |
| `driving` | The phone is being driven through the YouTube app. |
| `published` | Posted. Final. |
| `drafted` | Saved as a draft on the phone. Final. |
| `failed` | The run failed. Final. |
| `cancelled` | Cancelled before finishing. Final. |

Never say a Short is live before the status says `published`.

## When something goes wrong

- **A title error.** `Give the Short a title. YouTube names an untitled Short after the date.` means `caption` was missing. Over 100 characters is rejected too.
- **It stays in one status.** `phone-snapshot-tool` on the account's slot shows the screen,
  which usually explains it.
- **Stop it early.** `cancel-submission-tool` while `pending`, `ingesting` or `driving`,
  `delete-submission-tool` once it is final.
- **"Account not found".** The id belongs to another platform or another user.
- **The account has no phone assigned.** The call is refused until one is.

## Do not

- Do not call `start-rental-tool` or `request-phones-tool`. Those spend the user's money.
- Do not retry a failed submission automatically. A retry can post twice.

For TikTok, use the `0bull-tiktok-post` skill: captions there are optional and allow 2200
characters.
