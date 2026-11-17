# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube and other networks. This
skill uses it to keep each client's accounts in their own project, to get a connect link the client
opens themselves, to schedule approved clips on the client's accounts, and to read back each post's
status and numbers. It posts through each platform's own API with WoopSocial's approved apps, so the
agency needs no developer app or app review of its own. The exact fields live in WoopSocial's docs
and MCP schema (`schema_describe`); treat them as the source of truth if anything here looks
different.

WoopSocial posts what the agent sends. It doesn't write captions, cut clips or change files.

## 1. Is it connected?

Call `social_accounts_list`. If the tools aren't there, connect WoopSocial in this agent first.

Sign up: [app.woopsocial.com/signup](https://app.woopsocial.com/signup?utm_source=clipping-agency-skill&utm_medium=connect).
**Count the accounts first.** The free plan covers 2 social accounts. One client on TikTok, Reels
and Shorts is already 3, so an agency runs on a paid plan. At the time of writing (2026-11-16) Pro is
$19 a month for 20 accounts, which is six clients on three platforms, and every plan allows unlimited
projects ([pricing](https://woopsocial.com/pricing?utm_source=clipping-agency-skill&utm_medium=skill),
check it for today's numbers). Until then, every clip can be posted by hand from the schedule. Never
drop an account silently.

Setup for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=clipping-agency-skill&utm_medium=skill).
Give only the path for the agent you're running in:

| Agent | How to connect |
|---|---|
| Claude (claude.ai, Desktop, Cowork) | Add WoopSocial from the [Claude directory](https://claude.ai/directory/woopsocial), click Connect and sign in |
| Cursor | Install from [cursor.directory](https://cursor.directory/plugins/woopsocial-social-media-scheduler) and sign in |
| Claude Code | `claude mcp add --transport http woopsocial "https://api.woopsocial.com/mcp"`, then restart with `claude --continue`, `/mcp`, select woopsocial, Authenticate |
| Codex | `codex mcp add woopsocial --url https://api.woopsocial.com/mcp`, then `codex mcp login woopsocial`, then a new session (`codex resume --last` keeps this one) |
| OpenClaw | Install the [WoopSocial skill on ClawHub](https://clawhub.ai/woopsocial/skills/social-media-scheduler), or add the MCP URL to the agent's MCP config |
| Agents without sign-in support | Create an API key at [app.woopsocial.com/api-access](https://app.woopsocial.com/api-access) and use `https://api.woopsocial.com/mcp?api_key=YOUR_API_KEY` |

The API key is a password: never paste it into shared chats or commit it. Never restart the agent
while `make_clips.py` runs.

## 2. One project per client

- `projects_create` with `name` (the client's name). Projects keep each client's accounts, media and
  posts apart. Then `client.py project <client-id> <projectId>`. Never put two clients in one project:
  `client.py` refuses a project another client already has.
- Every request for a client uses only accounts in that client's project. WoopSocial requires all
  accounts of one request to be in the same project.

## 3. The client connects their own accounts

- `oauth_create_authorization` with `projectId` and `platform` (`TIKTOK`, `INSTAGRAM`, `YOUTUBE`)
  returns a link that opens in a browser. One per platform; leave out `redirectUrl`.
- Not verified end to end: no real outside client account has completed this flow yet. In a trial
  the TikTok link was TikTok's own authorize page and opened without a WoopSocial login; whether the
  callback completes for a person with no WoopSocial session, and how long the link stays valid,
  are unchecked. Check the first real client's connection with them. Only links for the client's real
  platforms ever go to a client: a sandbox (WOOPTEST) link opens WoopSocial's own login and is for the
  agency's own testing.
- The agency sends the links to the client (`client.py connect` prints a message to send). The client
  opens each one signed in to their own account and allows access. The permission screen names
  WoopSocial, not the agency, and the message says so up front, so the client isn't surprised by it.
  Nobody shares a password, which the platforms' terms forbid anyway.
- When the client is done: `social_accounts_list` with the `projectId`. Save the reply as it came back
  and run `client.py accounts <client-id> accounts.json`. Each account's `id` goes into the client's
  file and the ledger; an account another client already has is refused.
- TikTok: `social_accounts_get_platform_inputs` for the account returns the audiences it offers and its
  maximum video length. Save the reply and pass it to `client.py accounts` too. The client chooses
  from those audiences on the approval page.
- Instagram posting needs a Business or Creator account (free to switch in the Instagram app).

Not verified yet (check on a test account before relying on it): how long a connect link stays
valid, whether a link works the same for an account owned by someone outside the agency's WoopSocial
organisation, and what WoopSocial reports when a client removes the access on their side
(`client.py accounts` keeps each account's `status`; one that isn't `CONNECTED` is never posted to).

## 4. Upload each approved clip once

After `schedule.py <batch.json>` lists the files:

1. `media_uploads_create_session` with the client's `projectId` and `fileSizeInBytes` (the exact size
   `schedule.md` lists).
2. Save the response as `session.json` and run
   `python3 <skill>/scripts/upload_parts.py session.json <clip>`. It tries each part three times.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`; if not,
   poll `media_uploads_get_session`; on `FAILED` or `ABORTED`, report it.

Save `{"clips/clip-01.mp4": {"mediaId": "...", "sha256": "<the fingerprint schedule.md lists>"}}` as
`media.json` in the episode folder and run `schedule.py <batch.json> --media media.json`. A clip cut
again after its upload is refused. `upload_parts.py` prints the SHA-256 of the bytes it sent and keeps
it in `uploaded.json` next to `batch.json`; `schedule.py` refuses a file whose bytes aren't the ones
uploaded. Upload one file at a time: parallel uploads on one key can get
HTTP 429. Networks with an allowlist must allow `*.r2.cloudflarestorage.com`.

## 5. One request per clip, a child per account

`schedule.py` writes `requests/clip-NN.json`: one post scheduled for later, with a child for each of
the client's connected accounts, each with its own caption in `contentOverride`.

```json
{
  "content": [{"text": "<TikTok caption>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip>"}]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-10-06T16:30:00Z"},
  "socialAccounts": [
    {"platform": "TIKTOK", "socialAccountId": "<id>", "postType": "VIDEO", "postMode": "DIRECT_POST",
     "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": false, "allowStitch": false,
     "isYourBrand": false, "isBrandedContent": false, "autoAddMusic": false,
     "contentOverride": [{"text": "...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip>"}]}]},
    {"platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "REEL",
     "contentOverride": [{"text": "...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip>"}]}]},
    {"platform": "YOUTUBE", "socialAccountId": "<id>", "title": "<title>", "privacy": "public",
     "madeForKids": false, "tags": ["<tag>"],
     "contentOverride": [{"text": "...", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<clip>"}]}]}
  ]
}
```

- `scheduledFor` is UTC and in the future; the schedule shows it in the client's time zone.
- The request is validated as a whole: if one account's part is invalid, nothing is created.
- TikTok: WoopSocial requires `platform`, `socialAccountId`, `postType`, `allowComment`, `allowDuet`,
  `allowStitch`, `isYourBrand`, `isBrandedContent` and `autoAddMusic` on every TikTok child.
  `privacyLevel`, comments, duets and stitches are the client's choices from the approval page,
  never defaulted; without them TikTok waits. `isBrandedContent` is TikTok's paid partnership label:
  `true` for a clip with a sponsor segment (and then the audience can't be "only me").
  `isYourBrand` is "Your brand": `true` only when the clip promotes the client's own business.
  `autoAddMusic` is always `false`.
- YouTube: `title` and `privacy` are required; `madeForKids` is the channel owner's answer. `category`
  is optional; the skill leaves it out so YouTube picks it.
- WoopSocial can't set these, so `schedule.md` lists them as steps in the apps after a sponsored clip
  is live: Instagram's paid partnership label, YouTube's "includes paid promotion" box.
- Send each request exactly as written. `schedule.py` replaces `requests/` on every run, and
  `--check` and `--posted` refuse a request edited after it was written. Requests are also removed
  when a reply is applied, a new page is made, a clip is cut again or the client is offboarded: a
  request written for an earlier state can't be sent.
- Each request's time is kept in the ledger as a planned slot until it is sent, so another episode of
  the same client planned meanwhile never gets the same time.

Always, in this order:

1. The client's yes is recorded (`approve.py --apply`) and the agency has seen `schedule.md`.
2. Upload (section 4), then `schedule.py <batch.json> --media media.json`.
3. Right before sending each request: `schedule.py <batch.json> --check requests/<name>`. It checks
   again, at that moment, that the clip's approval still holds, the client is still active, the
   accounts are this client's, no check fails now, the clip isn't already sent, and the time is at
   least 30 minutes away. Never send a request it refuses.
4. `posts_validate` with each exact body. If it forces a change, change the batch or the client file
   and run `schedule.py` again; a changed caption needs the client's yes again.
5. `posts_create`, then at once `schedule.py <batch.json> --posted requests/<name> <postId>`. If it
   refuses (an account that isn't this client's, a clip whose approval no longer matches, a client
   who is no longer active), call `posts_delete` with the post id right away: it works while every
   account of the post is still `NOT_STARTED`.
6. After the scheduled time, `posts_get` with the post id: `socialAccountPosts` has one entry per
   account with its `deliveryStatus` (`NOT_STARTED`, `SENDING`, `PUBLISHED`, `FAILED`) and, once live,
   its `externalPostUrl`. Save the reply as `status.json` and run
   `schedule.py <batch.json> --status status.json`.

## 6. Nothing goes out twice

- `schedule.py` leaves every clip the ledger records as scheduled, processing or live out of new
  requests.
- **Not sure a post went through:** call `posts_get` for the recorded post id. If the session ended
  between `posts_create` and `--posted`, call `social_account_posts_list` with the client's `projectId`
  and `deliveryStatus` `NOT_STARTED` and look for it before anything else. Never create it again to
  find out.
- **One account failed:** say why in plain words. A failed delivery can still have published: check
  `social_account_posts_list` for that account first. A failed post is planned again by the next
  `schedule.py` run; the client's yes still holds while the clip is unchanged.

## 7. One machine schedules per agency

The ledger (`~/.clipping-agency/ledger.json`) is one file on one computer. It is what stops one clip
going to two clients, an account being used for two clients, and two episodes getting the same slot.
So one person on one computer writes the requests and records the posts for the whole agency (or
point every machine at one shared ledger with `CLIPPING_AGENCY_LEDGER`, on a drive that syncs before
each run). Others can cut clips and make pages; `schedule.py --check` and `--posted` run where the
ledger is. A save that would drop another session's write is refused.

## 8. Cancelling and offboarding

- `posts_delete` with a post id removes a scheduled post while every account of it is still
  `NOT_STARTED`. Record it with `schedule.py <batch.json> --cancelled <postId>` (or, while
  offboarding, `client.py offboard <client-id> --cancelled <postId>`). A client's "skip" on a clip
  that is already scheduled marks the post `cancel_requested` and writes the delete request for you.
  A `schedule.py --status` refresh keeps `cancel_requested` (and prints CANCEL NOW again) until the
  post is cancelled, published or failed.
- In a sandbox trial, a post sent to publish now was still deleted when `posts_delete` came within
  about a second (it was still NOT_STARTED). Once any account of the post is published,
  `posts_delete` answers `POST_NOT_DELETABLE` ("post cannot be deleted in its current state"): a live
  post can't be deleted through WoopSocial. `schedule.py --status` then says LIVE, NOT CANCELLED.
  Tell the client the same day; the post is removed in the app on that account.
- `social_accounts_delete` with an account id removes WoopSocial's access to that account. Record it
  with `client.py offboard <client-id> --revoked <PLATFORM>`.
- Live posts stay on the client's accounts. Only the client deletes those, in the app.
- Before closing an offboarding: `social_account_posts_list` with the client's `projectId` and
  `deliveryStatus` `NOT_STARTED` must show nothing, since posts made on another computer aren't in
  this ledger. Then `client.py offboard <client-id> --done --nothing-waiting`. `client.py release
  <socialAccountId>` frees an offboarded client's account in the ledger, for when the same account is
  later connected for a new client.

## 9. Numbers for the report

`social_account_posts_list_analytics` (filter by `projectId`, `platform` or `socialAccountId`, and a
publish-date range `startDate` to `endDate`) returns per post its `externalPostUrl`,
`deliveryCompletedAt`, lifetime `metrics` and `metricsCollectedAt`. Save the reply as it came back
and pass it to `report.py`.

- Each item carries `postId`, `socialAccountPostId`, `socialAccountId`, `platform` and `text`
  (seen in a sandbox trial), but no `projectId`: the filter in the request is the only sign of the
  project. So save one reply per client, always filtered by that client's `projectId`, and keep it
  with the client. `report.py` matches each item by its link, then its `postId`; only an item with no
  `postId` falls back to its account and a delivery time within 30 minutes of a slot, and never to a
  cancelled or failed one.

- Collected about once a day; reading doesn't refresh it.
- `views`: plays on TikTok and YouTube; times shown (repeats included) on Instagram.
- Not verified yet: TikTok per-post views through this call, and how soon after posting the first
  numbers appear. A post without numbers is shown as missing, never estimated.

`social_accounts_get_analytics` (one account, a date range) returns daily account metrics, including
followers on Instagram, subscribers on YouTube, and followers on TikTok for TikTok for Business
accounts only. Save one reply per account for the month and pass them with `report.py --followers`.
The report shows the follower change only when the reply carries those numbers.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=clipping-agency-skill&utm_medium=skill
