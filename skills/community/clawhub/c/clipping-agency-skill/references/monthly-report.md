# The monthly report

```
report.py <client-id> --month YYYY-MM analytics.json [...] [--followers account-analytics.json ...]
          [--notes notes.md] [--allow-unknown]
```

Writes, in `clients/<client-id>/reports/`:

- `<month>.md` and `<month>.html`: **for the client.** The HTML is one file, light and dark, no
  scripts, with tables that turn into stacked rows on a phone. Clips are named by their hook and
  episode, never by internal ids.
- `<month>-agency.md`: **for the agency only.** What to chase before the next report: posts without
  numbers, replies without a received time, posts not made through the skill, statuses that are
  unknown. Never send this one.
- `<month>.json`: this month's totals, which next month's report reads to show last month next to
  it.

## Before it writes anything

- **Statuses are refreshed, not trusted.** The ledger says what was scheduled; the saved analytics
  say what went live. A post the analytics show counts as live, matched by its link, its postId, or
  its account and a delivery time within 30 minutes of the time it was scheduled for. A post whose
  time has passed in the month and that the analytics don't show has an unknown status: the report
  stops and says to run `posts_get` for it and `schedule.py <batch> --status reply.json`.
  `--allow-unknown` writes the report anyway, with those posts listed as not confirmed and left out.
- **The wrong project's reply is refused.** A saved analytics reply with posts on accounts that
  aren't this client's (another client's, or nobody's in the ledger) stops the report: save
  `social_account_posts_list_analytics` again with this client's projectId.

## Where the numbers come from

- **Delivery** from the refreshed statuses: a clip counts in the month it went live
  (`deliveryCompletedAt`, in the client's time zone), once, however many platforms it went to.
  Against the agreed number per month; when fewer went live, the report says why from what the
  files show: clips scheduled for later, clips waiting for the client's reply, clips being changed
  as asked, clips the client skipped, failed posts, no new episode received. Failed posts are listed
  by hook and platform.
- **Approval turnaround** from each episode's `approvals.json`: for every page sent in the month,
  from when it was marked sent to when the client's first reply was received (`--received` or the
  reply's `Date:`). A reply with no received time is left out of the turnaround and counted as
  unknown, never replaced by the time it was applied. Per page: approved by reply, posted on silence
  as agreed (never called "approved"), changes, skipped.
- **Views, likes, comments, shares** only from saved `social_account_posts_list_analytics` replies.
  Several files are fine; the newest `metricsCollectedAt` per post wins. The numbers are lifetime
  totals up to the collection date, and each clip shows how many days it had been live when they
  were counted.
- **Followers** only from saved `social_accounts_get_analytics` replies (`--followers`), one per
  account, covering the month: the first and last day's follower (or subscriber) count and the
  change. WoopSocial returns followers for Instagram and YouTube; TikTok only for TikTok for
  Business accounts. No reply, or no follower numbers in it: no followers section, and the agency
  notes say why.
- **Last month** from `reports/<previous month>.json` when that report was made: clips delivered,
  and each platform's median.

## What a view is

| Platform | A view in WoopSocial's analytics |
|---|---|
| TikTok | a play of the video |
| YouTube Shorts | a play of the Short |
| Instagram Reels | a time the Reel was shown, repeats included |

So the report gives views per platform and never adds them together. "Top clip" is per platform.
A median is shown only from 3 posts on a platform; with fewer it would just be one of them.

## Gaps, said plainly

- A post with no number in the saved reply is left out of the total, and the client report says how
  many. The agency notes name it: numbers are collected about once a day, so save the analytics
  again the next day; if one is still missing, ask the client for the figure from the app and say
  where it came from in the notes.
- A platform that isn't connected has no numbers here.
- Posts on the client's accounts not made through this skill are counted and left out.

Never estimate reach, round up, add numbers from another source into the totals, or promise growth.
Put anything else the agency wants to tell the client (what was tried, what is next) in `--notes`:
it appears under "From us", clearly apart from the numbers.

Not verified yet through WoopSocial's analytics calls (check on the first real report): TikTok
per-post views, how soon after posting the first numbers appear, and the exact shape of
`social_accounts_get_analytics` replies (the report reads any dated entries with a follower or
subscriber count).
