---
name: using-bulkpublish
description: Schedule, publish and analyse social media posts across 15 networks through BulkPublish. Use whenever the user wants to draft, queue, cross-post, retry or measure social content, or asks about their channels, queue or posting quota.
---

# Working with BulkPublish

BulkPublish schedules and publishes posts to 15 social networks from one place,
and reads the numbers back. This skill covers the tools available over MCP,
the shape of a post, what each network accepts, and the mistakes that produce
a rejected request.

Connect the hosted server at `mcp.bulkpublish.com/mcp` over Streamable HTTP.
Sign-in is OAuth, so there is no key to paste. To run the server locally
instead, start `@bulkpublish/mcp-server` over stdio with an API key from
Settings then Developer in the `BULKPUBLISH_API_KEY` environment variable.

## How to behave

These are not style preferences. Getting them wrong costs the user real posts
on real accounts.

1. **Show a draft before you schedule it, and never publish without being
   asked.** `create_post` with `status: "draft"` is the safe default and is
   what the tool does when status is omitted. `publish_post` sends
   immediately, to a live audience, and cannot be undone from here.
2. **Never invent a channel id.** Call `list_channels` and use what it
   returns. A guessed id either fails or posts to the wrong account.
3. **Ask before deleting.** `delete_post` on a published post does not
   retract what already went out.
4. **Adapt per network rather than pasting one text everywhere.** Use
   `platformContent` for per-channel copy. A 3,000-character LinkedIn post
   truncated into a tweet reads like a mistake, because it is one.
5. **Check the character limit before writing, not after.** The limits table
   below is the contract; an over-long post is rejected, not trimmed.
6. **Confirm every reply, message and comment deletion one by one.** They go
   to a real person immediately and cannot be unsent.
7. **Say what you did.** After creating posts, list what went where and when,
   so the user can correct you before anything publishes.

## Tools

The hosted server exposes 20 tools, or 27 where it serves the Inbox and
comment tools. The local package exposes 79, adding
labels, hashtag groups, templates, calendar notes, review and client-connect
links, channel sets, schedules, RSS autopost and quota.

**Posts**
```
create_post        create a draft or a scheduled post
update_post        change content, timing, channels or media
get_post           one post, with its per-channel results
list_posts         filter by status, channel, label, date, approval, assignee
publish_post       send now (irreversible)
retry_post         retry failed destinations
delete_post        remove a post
get_post_metrics   per-post numbers once published
get_queue_slot     the next free time in the queue
```

**Channels**
```
list_channels      connected accounts, with ids, platform and health
```

**Media**
```
upload_media            from a public URL or an absolute local path
create_media_upload     start a direct upload
finalize_media_upload   finish one
list_media              the library
```

**Analytics**
```
get_analytics      totals and per-platform breakdown for a date range
```

**Inbox and comments** (see the `manage-inbox` skill before sending anything)
```
list_conversations     DMs, reviews and comment threads
get_conversation       messages in one conversation
reply_to_conversation  send a DM or review reply now (cannot be unsent)
update_conversation    mark read, archive, snooze, assign
list_post_comments     comments on a published post
reply_to_comment       public reply under a comment (cannot be unsent)
moderate_comment       like, hide or delete a comment
```
The Inbox is part of the Pro and Business plans; comment replies are on every
plan except Free, and reading a post's comments works on every plan. A channel connected before message or comment access existed may
need reconnecting, and some networks do not allow DMs or replies yet. Always
show the exact text and recipient and get a yes before any reply or deletion.

**Interactive panels** (render in hosts that support MCP Apps)
```
compose_post  view_posts  view_channels  view_media  view_analytics
```

## Creating a post

```
content            post text; optional for media-only posts
channels           [{ channelId, platform }] from list_channels
status             "draft" (default) or "scheduled"
scheduledAt        ISO 8601; required when status is "scheduled"
timezone           IANA zone, e.g. "America/New_York"; defaults to UTC
mediaFileIds       [ids] from upload_media
labels             [label ids]
platformContent    per-platform text overrides
platformSpecific   per-platform options
postTypeOverrides  per-platform post type, e.g. reel instead of feed_photo
postFormat         "post" (default), "video", "reel", "story", "carousel", "thread"
threadParts        [{ content, mediaFileIds }]; required when postFormat is "thread", minimum 2
requestApproval    true holds a scheduled post for a teammate to approve
publishWhenApproved true publishes it the moment it is approved, even past its time
                   (set it for "post now, once approved", not for a chosen time)
```

Notes that catch people out:

- **The label field on create and update is `labels`.** The filter on
  `list_posts` is `labelId`. They are different names on purpose.
- **Every thread part is length-checked**, not only the first. An over-long
  part is rejected naming the part number, the platform and its limit. URLs
  count as 23 characters on X and Mastodon and their real length elsewhere.
- **YouTube and TikTok require video.** Do not include them in an
  image-only post.
- **Instagram defaults to `feed_photo`.** For video, set `postTypeOverrides`
  to `reel` or `feed_video`, or the post is rejected.

## Scheduling

`get_queue_slot` reads only `timezone`, `position` and `excludePostId`. It
does not take a channel or a date. `position` is `"next"` for the first free
slot or `"end"` for the bottom of the queue.

The normal flow is: get a slot, create the post as a draft with that time,
show it to the user, then update it to `scheduled` once they agree.

## Post status

```
draft       not going anywhere yet
scheduled   waiting for its time
publishing  going out now
published   all destinations succeeded
partial     some destinations succeeded, some failed
failed      no destination succeeded
processing  the network is still handling it (video encoding, for example)
```

`partial` and `processing` are real states and are easy to forget. A post
sitting in `processing` is not stuck; a `partial` post needs `retry_post`,
which retries only the destinations that failed.

Approval is separate from status. `approvalStatus` is `none`, `pending`,
`approved` or `rejected`. A `scheduled` post whose approval is `pending` or
`rejected` will not publish. Approved more than 15 minutes after its time, a
post goes back to draft for a new time unless it has `publishWhenApproved` or the
approver passes `whenLate: "publish"` to `approve_post` (`"hold"` forces draft).

## Networks

| Network | Characters | Threads | Post types |
|---|---|---|---|
| X | 280 | yes | tweet |
| Instagram | 2,200 | no | feed_photo, feed_video, reel, story, carousel |
| Facebook | 63,206 | no | post, reel, story |
| LinkedIn | 3,000 | no | post, multi_image, pdf_carousel, article |
| Threads | 500 | yes | text, image, video, carousel |
| Bluesky | 300 | yes | post |
| Mastodon | 500 | yes | post |
| TikTok | 2,200 | no | video, photo_slideshow |
| YouTube | 5,000 | no | video, short |
| Pinterest | 500 | no | pin, video_pin, carousel |
| Google Business | 1,500 | no | standard, event, offer |
| Discord | 2,000 | no | post |
| Telegram | 4,096 | no | post |
| Tumblr | 32,768 | no | post |
| Snapchat | 160 | no | story, saved_story, spotlight |

The platform key for Google Business is `gmb`, not `google_business`.

## Media

`upload_media` takes either a public `url` or an absolute `filePath`, not
both. Attach the returned id through `mediaFileIds`.

Uploaded media is kept by default. `deleteMediaAfterPublish` defaults to
**false**, so files stay in the library after their post goes out.

## Analytics

`get_analytics` takes a required `from` and `to` in ISO date form, plus
optional `channelIds`, `platforms`, `labelIds`, `postFormat`, `mediaType` and
`compare`. Set `compare: true` to get the previous equal-length window back
alongside the current one. It is only available for windows of 15 days or
fewer, so it answers "is this week better than last week", not month over
month.

Link clicks are reported separately from platform clicks. Do not add the two
together: one visit can appear in both.

## Plan limits

`-1` means unlimited, `0` means not available on that plan.

| | Free | Pro | Business |
|---|---|---|---|
| Channels | 3 | 30 | 75 |
| Accounts per network | 1 | 2 | 5 |
| Posts per day | 3 | 30 | unlimited |
| Posts per month | 30 | 900 | unlimited |
| Scheduled posts pending | 10 | unlimited | unlimited |
| Media storage | 100 MB | 2 GB | 10 GB |
| API requests per day | 30 | 5,000 | 50,000 |
| API keys | 1 | 5 | 10 |
| Repeating schedules | 0 | 10 | unlimited |
| Labels | 10 | 50 | unlimited |
| Team members | 1 | 3 | 10 |
| RSS feeds | 1 | 10 | 50 |
| RSS auto-publish | no | yes | yes |

Daily limits reset at midnight UTC. Storage is cumulative, so deleting old
media frees it.

## Mistakes that produce an error

- Using `cronExpression` or `content` on a repeating schedule. The fields are
  `frequency`, `timeOfDay`, `dayOfWeek`, `dayOfMonth` and `contentTemplate`.
  `frequency` is `daily`, `weekly`, `biweekly` or `monthly`.
- Passing `labelIds` in a create or update body. It is `labels` there.
- Passing a channel or a date to `get_queue_slot`.
- Writing `google_business` instead of `gmb`.
- Treating `partial` as success, or as total failure. It is neither.
- Scheduling without `scheduledAt`, or sending `scheduledAt` without setting
  `status` to `scheduled`.
- Assuming a post with `approvalStatus: "pending"` will go out. It will not.

## Recipes

**Post one thing, safely**
1. `list_channels`
2. `get_queue_slot` with the user's timezone
3. `create_post` as a draft, with `platformContent` per network
4. Show the user every variant and the time
5. `update_post` to `scheduled` once they agree

**Turn an article into a set of posts**
1. Read the article
2. `list_channels`
3. Write one variant per network, respecting each limit in the table above
4. One `create_post` with all channels and `platformContent`
5. Show all variants before scheduling anything

**Fix a bad day**
1. `list_posts` with `status: "failed"` and a recent `from` date
2. `get_post` on each to see which destinations failed and why
3. `retry_post` only where the cause looks temporary
4. Tell the user which ones need them to act, such as reconnecting an account

**Report on the month**
1. `get_analytics` for the range (`compare` works only for 15 days or fewer)
2. `list_posts` with `status: "published"` over the same range
3. `get_post_metrics` on the strongest few
4. Answer with their numbers, naming specific posts
