---
name: 0bull-tiktok-post
description: Publish a video to TikTok from a real rented iPhone through the 0bull MCP server, then follow the submission to a final status.
homepage: https://docs.0bull.net/mcp/overview
---

# Post to TikTok with 0bull

0bull rents real iPhones by the month. A post is published by driving the TikTok app on one
of those phones, so publishing is asynchronous: you queue a submission and poll it until it
reaches a final status.

## Before you start

The 0bull MCP server must be connected:

```bash
openclaw mcp add 0bull --url https://0bull.net/mcp --transport streamable-http
openclaw mcp login 0bull
```

If `list-accounts-tool` is missing, stop and tell the user to run those two commands. You
are authorized as that user, so you only ever see their accounts and phones.

## Publish a video

1. **Pick the account.** Call `list-accounts-tool` with `platform: "tiktok"` and use the
   account's `id` as `account_id`. If several accounts match what the user described, ask
   which one rather than guessing. A TikTok account is bound to a phone slot, and one slot
   holds up to four TikTok accounts.
2. **Provide the video** through exactly one of:
   - `video_url`: a public https URL the server downloads.
   - `upload_id`: call `create-upload-url-tool` (no parameters), then POST or PUT the raw
     video to the returned `upload_url` within 15 minutes, then pass the `upload_id`.

   Supplying both, or neither, is rejected.
3. **Write the caption** with the user, never invented on their behalf. It is optional and
   holds up to 2200 characters.
4. **Queue it.** Call `create-submission-tool` with `platform: "tiktok"`, `account_id`, the
   video and the `caption`. Add `draft: true` to save it in the TikTok app instead of
   posting. The call returns the submission immediately in `pending`; nothing is live yet.
5. **Poll** `get-submission-tool` with the returned `submission_id`. Publishing a real video
   takes minutes, so leave a second or two between calls.

## Statuses

| Status | Meaning |
| --- | --- |
| `scheduled` | Queued for a future run. |
| `pending` | Queued, not picked up yet. |
| `ingesting` | The video is being fetched or prepared. |
| `driving` | The phone is being driven through the TikTok app. |
| `published` | Posted. Final. |
| `drafted` | Saved as a draft on the phone. Final. |
| `failed` | The run failed. Final. |
| `cancelled` | Cancelled before finishing. Final. |

Report the final status plainly. Never say a video is live before the status says
`published`.

## When something goes wrong

- **It stays in one status.** Look at the phone: `phone-snapshot-tool` for the account's
  slot shows what the screen is doing. A login wall or a stuck dialog is obvious in the
  picture.
- **Stop it early.** `cancel-submission-tool` works while it is `pending`, `ingesting` or
  `driving`. Once a status is final, use `delete-submission-tool` instead.
- **"Account not found".** The id belongs to another platform or another user. Check that
  you passed a TikTok account id.
- **The account has no phone assigned.** The call is refused until one is.
- **Calls start failing in bursts.** The limit is 250 requests a minute.

## Do not

- Do not call `start-rental-tool` or `request-phones-tool`. Those spend the user's money.
  If more phones are needed, say so and let the user go to https://0bull.net.
- Do not retry a failed submission automatically. A failure usually means the phone needs
  attention, and a retry posts twice.

For YouTube Shorts, use the `0bull-youtube-post` skill: the title rules are different.
