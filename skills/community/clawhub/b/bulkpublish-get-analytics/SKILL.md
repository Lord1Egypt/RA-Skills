---
name: get-analytics
description: Pull analytics, engagement metrics, and performance data from BulkPublish. Use when the user asks about post performance or engagement.
---

# BulkPublish — Analytics Reference

## Tools

| Tool | Use for | Key params |
|---|---|---|
| `get_analytics` | Overall summary for a date range | `from`, `to` (ISO dates); optional `channelIds`, `platforms`, `labelIds`, `postFormat`, `mediaType`, `compare` |
| `get_post_metrics` | Single post engagement | `postId` |
| `get_quota_usage` | Plan limits and current usage | none |
| `list_posts` | Find posts to analyze | `status`, `approvalStatus`, `from`, `to`, `channelId`, `search` |

## get_analytics response shape

Returns: total posts, status breakdown (any of the 7 post statuses: draft, scheduled, publishing, published, processing, failed, partial), per-platform counts, daily post counts for the range.

Posts also carry `approvalStatus` (`none` default | `pending` | `approved` | `rejected`), which is separate from `status` — filter `list_posts` with `approvalStatus: "pending"` to see the team approval queue. Pending and rejected posts never publish on their own.

## get_post_metrics response shape

Returns per-platform: likes, comments, shares, impressions, reach, clicks, saves, videoViews, engagementRate.

Plus `linkClicks` (and `totals.linkClicks` / `totalLinkClicks`): clicks on
bulkpubli.sh short links, measured by BulkPublish rather than reported by the
platform.

### Never report a 0 without checking `supportedMetrics` first

Every platform entry carries two support fields:

- `metricsSupported` — `false` when the platform has no per-post statistics API at all.
- `supportedMetrics` — the list of metric keys that platform *can* populate.

All metric columns are stored as integers defaulting to `0`, so a metric the
platform never reports is indistinguishable from a real zero **unless you read
`supportedMetrics`**. A key that is not in that list is **not a measurement** —
say "not reported by <platform>" or show a dash. Reporting it as `0` tells the
user their post got zero engagement when the platform simply has no such metric.

### `linkClicks` is the one metric every platform has

`linkClicks` is measured by BulkPublish, not the platform, so it is populated
even for the platforms in the "reports nothing" row below, and `supportedMetrics`
always contains it. Two rules when reporting it:

- **Never add it to `clicks`/`totalClicks`.** Those are the platform's own click
  figures. One visit can register in both, so summing them double-counts.
- **A 0 here is ambiguous in a specific way**: it means no tracked clicks, which
  also happens when the organization has link tracking switched off or is on
  the Free plan (no short links there), when the
  post contained no links, or when shortening was skipped on that channel for
  exceeding its character limit. Bot and link-preview traffic is excluded by
  design. Say "no tracked link clicks" rather than "nobody clicked".

| Platform | Reports | Never reports |
|---|---|---|
| X | impressions, likes, comments, shares, saves (bookmarks) | reach, clicks, video views |
| YouTube | impressions, video views, likes, comments | reach, shares, saves, clicks |
| Instagram | impressions, reach, likes, comments, shares, saves | clicks, video views |
| Facebook | likes, comments, shares + impressions, reach, clicks¹ | saves, video views |
| LinkedIn (company pages) | impressions, reach, likes, comments, shares, clicks | saves, video views |
| TikTok | impressions, video views, likes, comments, shares | reach, saves, clicks |
| Threads | impressions, likes, comments, shares | reach, saves, clicks, video views |
| Pinterest | impressions, clicks, saves, likes, comments, video views | reach |
| Bluesky | likes, comments, shares, saves (bookmarks) | impressions, reach, clicks, video views |
| Mastodon | likes, comments, shares | everything else |
| Discord | likes (reaction counts), comments (thread replies) | everything else |
| Snapchat | impressions, reach, likes, comments, shares, clicks, video views | saves |
| Google Business, Telegram, Tumblr | *nothing* | — |
| LinkedIn personal profiles | *nothing* | — |

¹ Facebook's impressions/reach/clicks come from Page Insights and need the
`read_insights` permission. Without it they stay `0` — "may not be readable",
which is neither a dash nor a trustworthy figure.

`engagementRate` is derived from impressions, so it exists only where
impressions do — it is always `0` for Bluesky and Mastodon.

### Two more reasons a figure can legitimately be 0

- **Not synced yet.** Figures come from a snapshot refreshed every 6 hours, not a
  live read. A just-published post appears immediately with zeros.
- **Metrics sync switched off.** X reads are billed, so per-post sync is opt-in
  per channel and runs at most weekly. The engagement response lists affected
  channels in `metricsDisabledChannels`; until the user enables it on the
  Channels page, every X figure stays 0 and refreshing cannot change that.

## get_quota_usage response shape

Returns: plan name, limits (channels, posts/day, storage, API calls), current usage for each, subscription status.

## Patterns

- "How did my posts do this week?" → `get_analytics` with last 7 days
- "Which post got the most likes?" → `list_posts` (status: "published") then `get_post_metrics` for each
- "Am I near my limits?" → `get_quota_usage`
- Date params are ISO date strings: "2026-04-01", not datetime
