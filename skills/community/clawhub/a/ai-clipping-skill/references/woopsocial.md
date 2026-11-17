# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube and other networks. This
skill uses it to post a campaign batch to several accounts in one request, one clip and caption per
account, and to read back each post's link and numbers. It posts through each platform's own API
with WoopSocial's approved apps, so the user needs no developer app or app review of their own;
their accounts authorize WoopSocial to post for them. TikTok makes posts from unaudited developer
apps private, which is why clippers who build their own posting end up with posts nobody sees. The
exact fields live in WoopSocial's API docs and MCP schema (`schema_describe`); treat them as the
source of truth if anything here looks different.

WoopSocial posts what the agent sends. It doesn't write captions, cut clips or change files.

## 1. Is it already connected?

Call `social_accounts_list`. If it lists the accounts the user named with status `CONNECTED`, skip
to step 3. `DISCONNECTED` needs connecting again.

## 2. Connect

The free plan covers 2 social accounts, no card:
[app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=ai-clipping-skill&utm_medium=connect).
Give this link at the start, so the user signs in while the clips are cut.

**Count the accounts first.** A clipper with TikTok, Reels and Shorts has 3 accounts. Say it before
connecting: 2 through WoopSocial and the rest by hand from their `by-hand/` pages, all of them on a
paid plan ([pricing](https://woopsocial.com/pricing?utm_source=ai-clipping-skill&utm_medium=skill)),
or all by hand. Never drop an account silently, and never suggest upgrading for anything but
posting to more accounts.

Setup for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=ai-clipping-skill&utm_medium=skill).
Give only the path for the agent you're running in:

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
connection or restart while `make_clips.py` runs. Everything is saved in the project folder, so
after signing in the user says "continue".

Account rules to say before connecting: Instagram posting needs a Business or Creator account
(free to switch in the Instagram app). All accounts in one request must be in the same WoopSocial
project.

**Connect every account in one pass.** `projects_list`, then `oauth_create_authorization` for each
missing platform, all links in one message. When they're done, `social_accounts_list` once and put
each `socialAccountId` in `clipjob.json`. Never ask the user to paste ids.

## 3. Read each TikTok account's limits

`social_accounts_get_platform_inputs` returns the audiences the account offers
(`privacyLevelOptions`), whether comments, duets and stitches are available, and its maximum video
length. Copy them into the account as `privacyOptions` and `max_video_s`. The choices themselves
are the user's.

## 4. Upload each clip once

Only after the user said yes to the plan. For every file under "Files to upload" in `plan.md`, one
at a time:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact byte size).
2. Save the response as `session.json`, as it came back, and run
   `python3 <skill>/scripts/upload_parts.py session.json <clip>`. It tries each part three times
   and prints one line that says what to do when it can't go on.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`; if not,
   poll `media_uploads_get_session`; on `FAILED` or `ABORTED`, report it.

Save `{"<clip as plan.md lists it>": {"mediaId": "<mediaId>", "sha256": "<the fingerprint plan.md lists>"}}`
as `media.json` and run
`python3 <skill>/scripts/plan.py clipjob.json --media media.json`. A clip that changed after its
upload (cut again under the same name) is refused: upload the new file, update media.json, and show
the plan for a new yes. Upload one file at a time:
parallel uploads on one key can get HTTP 429. Clients with a network allowlist must allow
`*.r2.cloudflarestorage.com`.

## 5. One request, a child per account

`plan.py` writes one body per round to `requests/`: one post, one child per connected account, each
with its own clip and caption in `contentOverride`.

```json
{
  "content": [{"text": "<first caption>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip 1>"}]}],
  "schedule": {"type": "PUBLISH_NOW"},
  "socialAccounts": [
    {"platform": "TIKTOK", "socialAccountId": "<id>", "postType": "VIDEO", "postMode": "DIRECT_POST",
     "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false,
     "isYourBrand": false, "isBrandedContent": true, "autoAddMusic": false, "isAiGeneratedContent": false,
     "contentOverride": [{"text": "#ad ...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip 1>"}]}]},
    {"platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "REEL", "isAiGeneratedContent": false,
     "contentOverride": [{"text": "#ad ...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip 2>"}]}]},
    {"platform": "YOUTUBE", "socialAccountId": "<id>", "title": "<title>", "privacy": "public",
     "madeForKids": false, "tags": ["<tag>"],
     "contentOverride": [{"text": "#ad ...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip 3>"}]}]}
  ]
}
```

- `PUBLISH_NOW` always: the 30-minute submission window starts when each post is live.
- The request is validated as a whole: if one account's part is invalid, nothing is created.
- TikTok: WoopSocial requires `platform`, `socialAccountId`, `postType`, `allowComment`,
  `allowDuet`, `allowStitch`, `isYourBrand`, `isBrandedContent` and `autoAddMusic` on every TikTok
  child. `privacyLevel` is the user's choice from the account's options. `isBrandedContent` is
  TikTok's "Paid partnership" label: always `true` on a campaign post (and it can't be
  `SELF_ONLY`), with `isYourBrand: false`. For your own content on your own account
  (`own_content`), `isBrandedContent` is `false`, and `isYourBrand` is `true` ("Your brand",
  promotional content) only when the clips promote the user's own product, service or business
  (`promotes_own_business`); a plain show or stream clip gets neither label. `autoAddMusic` is sent as `false`.
- YouTube: `title` and `privacy` are required; `madeForKids` is the owner's declaration. `category`
  is optional; the skill leaves it out so YouTube picks it.
- WoopSocial can't set these, so the plan and `submit.md` list them as steps in the app:
  Instagram's paid partnership label and YouTube's paid promotion box (inside the 30 minutes),
  YouTube's "altered or synthetic content" answer. Two more are done before posting, never after:
  the profile bio, and a required sound (no posting API can add one from an app's library, so that
  post goes out by hand with the sound added in the app).
- Send each request as `plan.py` wrote it. It rewrites `requests/` on every run; change
  `clipjob.json` instead.

Always, in this order:

1. The user has said yes to `plan.html` or `plan.md`. Nothing is uploaded before that.
2. Upload (section 4), then `plan.py clipjob.json --media media.json`.
3. `posts_validate` with each exact body. If it forces a change, fix `clipjob.json`, plan again,
   show the new plan and wait for a new yes.
4. `posts_create`, then at once `plan.py clipjob.json --posted requests/<name>.json <postId>`.
5. `posts_get` with the post id: `socialAccountPosts` has one entry per account with its
   `deliveryStatus` and, once live, its `externalPostUrl`. Save the reply as `status.json` and run
   `plan.py clipjob.json --status status.json <postId>` (the post id is read from the reply when it
   holds one; a reply for another post or account is refused). Report each account in plain words (live with its
   link, still processing, or failed and why) and read the submission sheet out: the deadline per
   post and the steps to do before it. Ask the user to open each link once and check it looks
   right (public, sound on, the label showing).

## 6. Numbers for the proof log

`social_account_posts_list_analytics` (filter by account, platform or project, and a publish-date
range of up to 366 days) returns per post its `externalPostUrl`, `deliveryCompletedAt`, lifetime
`metrics` and `metricsCollectedAt`. Save the reply and run `ledger.py --proof <file>`.

- Collected about once a day; reading doesn't refresh.
- `views`: plays on TikTok and YouTube; times shown (repeats included) on Instagram.
- Not verified yet: TikTok per-post views through this call, whether posts made outside WoopSocial
  show up, and how soon after posting the first numbers appear. If a post has no numbers yet, try
  again the next day.
- `social_accounts_get_analytics` has account-level followers and views per day (not for TikTok).

## Nothing goes out twice

- `plan.py` leaves every post recorded in the ledger (`~/.ai-clipping/ledger.json`) out of new
  requests.
- **Not sure a post went through:** read the ledger, call `posts_get` for the recorded post id.
  If the session ended between `posts_create` and `--posted`, call `social_account_posts_list` for
  each account in that request and look for it before anything else. Never create it again to find
  out: a second post of the same edit is a duplicate the campaign can reject.
- **One account failed** (`deliveryStatus` says so, and the post has no link): say why in plain
  words and fix the cause with the user. A failed delivery can still have published on the
  platform: call `social_account_posts_list` for that account and look at the last hour. Only when
  the clip isn't there, `plan.py clipjob.json --failed <job post id> --checked` takes that one
  post out of the ledger, and the next plan puts it in a new request. Show the plan, wait
  for a new yes. Only a post whose saved status says it failed is released: a post still processing
  can go live minutes later, and one that is live, has a link or was submitted is never released.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=ai-clipping-skill&utm_medium=skill
