# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn
(profiles and Pages), X, Pinterest, Threads and Bluesky. This skill uses it to post or schedule
one video to several accounts in one request and to read the results back. It posts through each
platform's own API with WoopSocial's approved apps, so the user needs no developer app or app
review of their own. The user's accounts authorize WoopSocial to post for them. The exact fields
live in WoopSocial's API docs and MCP schema (`schema_describe`); treat them as the source of truth
if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user named with status
`CONNECTED`, skip to step 3. An account listed as `DISCONNECTED` needs connecting again.

## 2. Connect

The free plan includes MCP access for 2 social accounts, no card needed. New users can make the
account first:
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=cross-post-video-skill&utm_medium=connect),
or sign up in the same browser window as the sign-in.

**Count the accounts first.** TikTok, Reels and Shorts are 3 accounts. If the job uses more than 2,
say so before connecting and let the user choose: connect 2 now and post the others by hand from
their `by-hand/` pages, or upgrade at
[pricing](https://woopsocial.com/pricing?utm_source=cross-post-video-skill&utm_medium=skill). Never
drop an account silently, and never suggest upgrading for anything but posting to more accounts.

Setup for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=cross-post-video-skill&utm_medium=skill).

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
connection or restart while a script runs. Everything is saved in the project folder, so after
signing in the user says "continue".

**Account rules to say before connecting:**

- Instagram posting needs a Business or Creator account; no app can post to a personal account.
  Switching is free in the Instagram app: Settings and activity > Account type and tools > Switch
  to professional account.
- Facebook posts go to a Page; Meta doesn't let apps post to personal profiles.
- All accounts in one request must be in the same WoopSocial project.

**Connect every account in one pass.** Find the project with `projects_list`, then call
`oauth_create_authorization` for each platform that is missing and give the user all the links in
one message. When they say they're done, call `social_accounts_list` once and put each
`socialAccountId` in `crosspost.json`. If a link has expired, make a new one. Never ask the user to
paste IDs.

## 3. Read each account's limits

For each TikTok account, `social_accounts_get_platform_inputs` returns the audiences it offers
(`privacyLevelOptions`), whether comments, duets and stitches are available, and its maximum video
length. Copy them into the account as `privacyOptions` and `max_video_s`. For Pinterest it returns
the boards. Read them again before each batch; they change.

## 4. Upload each file once

For every file under "Files to upload" in `plan.md` (the video and the cover), one at a time:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact byte size).
2. Save the response as `session.json`, as it came back, and run
   `python3 <skill>/scripts/upload_parts.py session.json <file>` (both paths are relative to the
   folder you run from). It tries each part three times. When it can't go on it prints one line
   that says why and what to do: a new session when the upload link has expired, the same command
   again after a network problem.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`; if not,
   poll `media_uploads_get_session`; on `FAILED` or `ABORTED`, report it.

Upload only after the user has said yes to the plan. Save `{"<file as in plan.md>": "<mediaId>"}` for every file as `media.json` and run
`python3 <skill>/scripts/plan.py crosspost.json --media media.json`. One upload serves every account.
`media.json` is looked for in the folder you run from, then next to `crosspost.json`. Every name in
it must be a file of the plan, written as `plan.md` lists it; any other name is an error.
Upload one file at a time: parallel uploads on one key can get HTTP 429. Clients with a network
allowlist must allow `*.r2.cloudflarestorage.com`.

## 5. One request, a child per account

`plan.py` writes one body per video and time to `requests/`. The post has one child per account,
and each child carries its own text in `contentOverride`:

```json
{
  "content": [{"text": "<TikTok caption>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video>"}]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-20T17:00:00Z"},
  "socialAccounts": [
    {"platform": "TIKTOK", "socialAccountId": "<id>", "postType": "VIDEO", "postMode": "DIRECT_POST",
     "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false,
     "isYourBrand": false, "isBrandedContent": false, "autoAddMusic": false, "isAiGeneratedContent": false,
     "cover": {"type": "MEDIA_LIBRARY", "mediaId": "<cover>"},
     "contentOverride": [{"text": "<TikTok caption>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video>"}]}]},
    {"platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "REEL", "isAiGeneratedContent": false,
     "cover": {"type": "MEDIA_LIBRARY", "mediaId": "<cover>"},
     "contentOverride": [{"text": "<Reels caption>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video>"}]}]},
    {"platform": "YOUTUBE", "socialAccountId": "<id>", "title": "<title>", "privacy": "public",
     "madeForKids": false, "tags": ["<tag>"], "category": "28",
     "contentOverride": [{"text": "<description>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<video>"}]}]}
  ]
}
```

- `schedule`: `{"type": "PUBLISH_NOW"}` or `SCHEDULE_FOR_LATER` with `scheduledFor` (UTC, in the
  future). Accounts with different times get separate requests.
- The request is validated as a whole: if one account's part is invalid, nothing is created.
- TikTok: `privacyLevel` must be one of the account's options and is the user's choice.
  `isYourBrand` is TikTok's "Promotional content" label, `isBrandedContent` its "Paid partnership"
  label (which can't be `SELF_ONLY`).
- TikTok drafts: `postMode` `DIRECT_POST` publishes. `MEDIA_UPLOAD` sends the video to the
  account's TikTok inbox as a draft: the user gets a notification, opens it in the app, adds a
  sound, pastes the caption (video drafts arrive without one), picks who can see it and posts.
  `plan.py` writes it for a video with `"tiktok_draft": true`. The draft lands at the scheduled
  time, not the post time, so `plan.py` schedules it 2 hours before the time in the job. At most 5
  drafts wait per account per 24 hours. The draft child follows WoopSocial's `posts_create` schema:
  `autoAddMusic` is a required TikTok field, so it is sent as false, and `privacyLevel` is optional,
  so it is left out (the user picks the audience in the app). This body was checked against the
  schema but not yet posted to a real TikTok account.
- Instagram: `postType` `REEL`; optional `trialParams` `{"graduationStrategy": "MANUAL"}` posts a
  Trial Reel.
- The cover image (`cover`) and the AI flag (`isAiGeneratedContent`) are sent as WoopSocial's
  schema defines them. After the first post to a new account, have the user look at the live post
  once to confirm the cover and the AI label look right.
- YouTube: `title` and `privacy` are required; `madeForKids` is the owner's declaration.
- Facebook: `postType` `REEL` (vertical, 3 to 90 s) or `VIDEO`. Pinterest: `pinterestBoardId`,
  `title`, optional `link`.
- Not available through WoopSocial, so `plan.md` lists them under "After it's live": the YouTube
  cover, YouTube's "Altered content" and "Paid promotion" answers, Instagram's paid partnership
  label. Also not available: choosing a sound (for TikTok, send a draft and add it in the app),
  Instagram collaborators, a first comment.
- Send each request as `plan.py` wrote it. `plan.py` rewrites `requests/` on every run, so a change
  made by hand in a request file is lost; change `crosspost.json` instead.

Always, in this order (the same order as SKILL.md, Step 7):

1. The user has said yes to `plan.html` or `plan.md`. Nothing is uploaded before that.
2. Upload (section 4), then `plan.py crosspost.json --media media.json`.
3. `posts_validate` with each exact body. If it forces a change, fix `crosspost.json`, plan again,
   show the user the new plan and wait for a new yes. If nothing changed, the yes covers it.
4. `posts_create` per request, then at once
   `python3 <skill>/scripts/plan.py crosspost.json --posted requests/<name>.json <postId>`
   (the post id can't be empty). See "Nothing goes out twice" below.
5. `posts_get` with the post ID: `socialAccountPosts` has one entry per account with its
   `deliveryStatus` (`NOT_STARTED`, then `PUBLISHED` or a failure) and, once live, its
   `externalPostUrl`. Processing takes a few minutes on TikTok and Instagram. Report each account
   in plain words: live (with its link), scheduled for when, still processing, or failed and why
   (a disconnected account, a platform limit, too many posts today). These two fields are all the
   status there is: they don't say who can see the post or whether the sound plays, so give the
   user each link and ask them to open it once and check it looks right (visible to who it should
   be, sound on, the right cover). Report anything off as a problem, not a success.

A scheduled post can only be checked after its time. Say so, and tell the user what to say later:
"These go out Fri 13 Nov 18:00. After that, say 'check my cross-post' and I'll read the result per
account." If you can set a reminder or a scheduled task, offer one for 15 minutes after the latest
time. On "check my cross-post", in this session or a later one: read `posted.json`, call
`posts_get` for each recorded post id, report one line per account as in step 5, then read the
"After it's live" list from the plan. Never create anything to find out.

## 6. Results

`social_account_posts_list` (filter by `socialAccountId` or `postId`) returns each post with the
numbers the platform shares (views, likes, comments, shares where available) under `analytics`.
Give a video a few days. Compare each account with its own earlier posts; the same video does
differently on each platform, and that says little about the video.

## Nothing goes out twice

`--posted` records the video for every account in that request in `posted.json`, one entry per
video and account (`references/job-file.md` shows the file). From then on `plan.py` leaves those
accounts out of every new request for that video and shows them on the plan as "already posted",
"scheduled" or "sent as a draft", with the post id. It does not matter what changes afterwards: the
time, a connected account's name, or the other accounts in the job.

- **A third account connected later** (the usual step after the free plan's 2 accounts): add its
  `socialAccountId`, run `plan.py` again, and the new request holds only that account.
- **Not sure a post went through:** read `posted.json` and call `posts_get` for the recorded post
  id before anything else. Never create a request again to find out.
- **The session ended between `posts_create` and `--posted`** (no post id in `posted.json`, and
  the plan still has the request): call `social_account_posts_list` for each account in that
  request (filter by `socialAccountId`) and look for the post. If it is there, check it with
  `posts_get` and record it with `plan.py crosspost.json --posted requests/<name>.json <its postId>`;
  only if no account has it, create the request.
- **One account failed** (the others went through): fix the cause with the user (reconnect the
  account, a shorter cut, try tomorrow after "too many posts today"), then
  `plan.py crosspost.json --failed <request or video id> "<account name>"` removes that account's
  entry for that video. Plan again: the new request holds only that account. Show the plan; after
  a new yes, upload nothing new (the `media.json` from before still works), validate, create and
  record it. If validation changes the request, show it again: the yes must cover the request you
  create. Never release an account whose post is live, scheduled or still processing.
- **Posted by hand:** `plan.py crosspost.json --posted-by-hand <video id> "<account name>"`
  records it with the account's platform. It is matched by name and platform until the account is
  connected; then `plan.py` moves it to the account's id, so a later rename changes nothing. A
  record that matches no account in the job is a warning that names it (`references/job-file.md`).
- **Posting the same video to the same account again on purpose:** only when the user asks.
  Release it with `--failed` as above, run `plan.py` again, show the plan, wait for a yes.
- **A new video under an old id:** `plan.py` stops ("video id 'a' was already posted from a
  different file; give this video a new id"). Give it its own id; never reuse one.
- `posted.json` is never emptied by `plan.py`; it is rewritten only to move a by-hand entry to the
  account's id. If it can't be read, `plan.py` stops.

## Changing a scheduled post

Not live yet: there's no edit, so after confirming with the user delete it with `posts_delete`,
release each of its accounts with `plan.py crosspost.json --failed <video id> "<account name>"`,
change `crosspost.json`, plan again, show the plan, and create it again after a new yes. Already
live: change it in the app.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=cross-post-video-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=cross-post-video-skill&utm_medium=skill
