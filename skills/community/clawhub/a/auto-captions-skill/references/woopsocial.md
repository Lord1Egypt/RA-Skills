# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn
(profiles and Pages), X, Pinterest, Threads and Bluesky. This skill uses it to post or schedule
the captioned videos and to read results back. It posts through each platform's own API with
WoopSocial's approved apps, so the user needs no developer app or app review of their own. The
exact fields live in WoopSocial's API docs and MCP schema (`schema_describe`); treat them as the
source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user wants, skip to step 3.

## 2. Connect

The free plan includes MCP access for 2 social accounts with unlimited posts (on X the first few
posts are free, then it's credit-based), no card needed. New users can make the account first:
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=auto-captions-skill&utm_medium=connect),
or sign up in the same browser window as the sign-in.

**Count the accounts in the plan first.** If it uses more than 2, say so before connecting ("the
plan uses 3 accounts; the free plan covers 2") and let the user choose: connect 2 now and keep the
others in the plan (they stay listed under "Not connected yet"), or upgrade at
[pricing](https://woopsocial.com/pricing?utm_source=auto-captions-skill&utm_medium=skill). Never
drop an account from the plan silently, and never suggest upgrading for anything but posting.

Setup for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=auto-captions-skill&utm_medium=skill).

Give the user only the path for the agent you're running in:

| Agent | How to connect |
|---|---|
| Claude (claude.ai, Desktop, Cowork) | Add WoopSocial from the [Claude directory](https://claude.ai/directory/woopsocial), click Connect and sign in |
| Cursor | Install from [cursor.directory](https://cursor.directory/plugins/woopsocial-social-media-scheduler) and sign in |
| Claude Code | `claude mcp add --transport http woopsocial "https://api.woopsocial.com/mcp"`, then restart with `claude --continue` (keeps the conversation), `/mcp`, select woopsocial, Authenticate |
| Codex | `codex mcp add woopsocial --url https://api.woopsocial.com/mcp`, then `codex mcp login woopsocial`, then start a new session (`codex resume --last` keeps this one) |
| OpenClaw | Install the [WoopSocial skill on ClawHub](https://clawhub.ai/woopsocial/skills/social-media-scheduler), or add the MCP URL to the agent's MCP config |
| Agents without sign-in support | Create an API key at [app.woopsocial.com/api-access](https://app.woopsocial.com/api-access) and use `https://api.woopsocial.com/mcp?api_key=YOUR_API_KEY` |

The API key is a password: never paste it into shared chats or commit it. Claude Code and Codex
load new tools only in a new session, and a restart stops a running script: never add the
connection or restart while a script runs (transcription or render). Everything is saved in the project folder, so after
signing in the user says "continue".

**Account rules to say before connecting:**
- Instagram posting needs a Business or Creator account; no app can post to a personal account.
  Switching is free in the Instagram app: Settings and activity > Account type and tools > Switch
  to professional account.
- Facebook posts go to a Page; Meta doesn't let apps post to personal profiles.
- TikTok asks who can see each post (`privacyLevel`), and YouTube asks whether a video is made for
  kids (`madeForKids`); the user answers both.

**Connect every account in the plan in one pass.** Once WoopSocial is connected, find the project
with `projects_list`, then call `oauth_create_authorization` for every platform under "Not
connected yet" in `plan.md` (TIKTOK, INSTAGRAM, YOUTUBE, FACEBOOK, LINKEDIN, LINKEDIN_PAGES, X,
THREADS, BLUESKY) and give the user all the links in one message. When they say they're done, call
`social_accounts_list` once, put each `socialAccountId` in `post.json`, run `post_plan.py` again,
and go straight on to uploading and validation, so the plan is scheduled in the same sitting. If a
link has expired, make a new one. Never ask the user to paste IDs.

## 3. Upload each video once

For every file listed under "Files" in `plan.md`, one at a time:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact byte size).
2. Save the response as `session.json` and run
   `python3 <skill>/scripts/upload_parts.py session.json <file>`.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`; if
   not, poll `media_uploads_get_session`; on `FAILED` or `ABORTED`, report it.

Save `{"<file as in plan.md>": "<mediaId>"}` for every file as `media.json` and run
`python3 <skill>/scripts/post_plan.py post.json --media media.json`. One upload serves every
account that posts the same file. The free plan has 1 GB of media storage; for a big batch, set
`autoDeleteMediaAfterPublish` to true on each file's last post. Upload one file at a time: parallel uploads on one key can get
HTTP 429. Clients with a network allowlist must allow `*.r2.cloudflarestorage.com`.

## 4. Validate, confirm, schedule

`post_plan.py` writes one body per post to `requests/captions/`:

```json
{
  "content": [{"text": "<post text>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<id>"}]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-23T23:00:00Z"},
  "socialAccounts": [{"platform": "TIKTOK", "socialAccountId": "<id>", "postType": "VIDEO",
                      "postMode": "DIRECT_POST", "privacyLevel": "PUBLIC_TO_EVERYONE",
                      "allowComment": true, "allowDuet": true, "allowStitch": true,
                      "isYourBrand": false, "isBrandedContent": false, "autoAddMusic": false}],
  "autoDeleteMediaAfterPublish": false
}
```

- Instagram: `"postType": "REEL"`. YouTube: `title`, `privacy`, `madeForKids`, optional `category`.
  Facebook: `"postType": "REEL"` (vertical, 3 to 90 s) or `"VIDEO"`. LinkedIn, X, Threads, Bluesky:
  no extra fields.
- `"autoDeleteMediaAfterPublish": true` removes the files from the WoopSocial media library once
  every post using them is published (only when no later post reuses the same mediaId).
- WoopSocial posts the video and the post text. It doesn't attach subtitle files; add the SRT in
  YouTube Studio or Facebook where `plan.md` says. X and LinkedIn take a subtitle file only while
  uploading in their own app, so there the burned-in captions do the job.

Always:

1. `posts_validate` with each exact body. Fix anything it rejects.
2. Show `plan.md` (what goes where and when) and wait for one clear yes for the batch. A change
   means new requests and a new validation.
3. `posts_create` per request; keep each post ID; `posts_get` for the status. Report failures in
   plain words (a disconnected account, a platform limit).

Optional: `retryPolicy` (`maxRetries`, `delaySeconds`) makes WoopSocial retry a failed delivery.

## 5. Results

`social_account_posts_list` (filter by `socialAccountId` or `postId`) returns each post with the
numbers the platform shares (views, likes, comments, shares where available) under `analytics`.
Compare a captioned video with the same account's own earlier videos, never with other accounts,
and give it at least a week.

## Changing a scheduled post

Not live yet: there's no edit, so delete it with `posts_delete` and create it again, after
confirming with the user. Already live: change it in the app.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=auto-captions-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=auto-captions-skill&utm_medium=skill
