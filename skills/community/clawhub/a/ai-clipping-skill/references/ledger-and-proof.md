# Submitting, the ledger, proof and earnings

## The 30 minutes

Most campaigns accept a post only when its link is submitted within 30 minutes of it going live,
and a post goes into one campaign, once, ever. A late or misrouted post can't be fixed: the only
way back is a new edit, posted fresh. That is why every campaign post goes out "now", never
scheduled, and why the manual steps (Instagram paid partnership label, YouTube paid promotion,
the bio link) are done inside the same window.

After `posts_create`:

1. `plan.py clipjob.json --posted requests/<name>.json <postId>` records each account's post in
   the ledger with the clip's fingerprint, the source footage it used, the caption and the time.
2. A minute later, `posts_get <postId>`; save the reply as `status.json` and run
   `plan.py clipjob.json --status status.json <postId>`. It fills in each post's link and the time it went
   live (`deliveryCompletedAt` when the reply has it; otherwise the time it was recorded, marked
   "about") and writes `submit.md`: per post the link, the clock time the window closes in the
   user's time zone (with EST/EDT, so the night the clocks change can't fool anyone), the campaign,
   the steps to do before then, the screenshot times and the evidence folder per post. A post still
   processing has no clock until it is live.
3. The user pastes each link into the campaign (the skill never does this and never drives the
   user's logged-in browser; no marketplace has a submission API for clippers). Then:
   `ledger.py --submitted <link> --campaign <id> [--submission-id <id>]`.

By hand: `plan.py clipjob.json --posted-by-hand <job post id> <link>` (add `--at <time>` if it went
live a while ago; a time without an offset, like `2026-11-16T09:05`, is read in the job's time zone
and the output says so; a date alone or a time in the future is refused) records it and prints the
deadline.

## The ledger

One file for every campaign, whatever folder each lives in: `~/.ai-clipping/ledger.json` (the
`.ai-clipping` folder in the user's home folder, on Windows too). `AI_CLIPPING_HOME` moves the
folder, `AI_CLIPPING_LEDGER` or `--ledger <file>` on any script names another ledger file (the
example uses its own). Links are matched on the platform and the post id, so
`?igsh=...`, `?si=...`, `?is_from_webapp=1` and `utm_` tags don't make a second post. Share links
(`vm.tiktok.com/...`) are refused: open them and copy the full link.

```json
{
  "posts": {
    "<postId>|<socialAccountId>": {"postId": "...", "job_post": "groundhog-tiktok",
      "campaign": "orbit-crew-dragon", "account": "TikTok", "platform": "TIKTOK",
      "file": "clips/clip-01.mp4", "sha256": "...", "source_file": "interview.mp4",
      "source_sha256": "...", "ranges": [[490.0, 513.4]], "hook": "...", "caption": "...",
      "url": "https://...", "published_at": "2026-11-16T14:01:40Z", "recorded": "..."}
  },
  "submissions": [
    {"url": "https://...", "campaign": "orbit-crew-dragon", "submitted_at": "...",
     "post": "groundhog-tiktok", "account": "TikTok"}
  ]
}
```

What it stops:

- `ledger.py --submitted` refuses a link already submitted (to this or any campaign), a post that
  was made for another campaign, and a link while a recent post of that platform (and, for TikTok,
  that handle) still has no link in the ledger: run `plan.py --status` first, so the skill knows
  which post it is. A late submission is recorded with a warning.
- `check_clips.py` refuses an edit (same sha256) that is already posted, on another account or for
  another campaign; footage that overlaps a posted edit of this campaign on another account of the
  same platform; and the same moment posted again on the same account under a new post id.
- `plan.py` leaves a post that is already recorded out of every new request.
- Two sessions at once (two agents, two campaigns): every save takes a lock file and checks that
  nobody wrote the ledger since it was read. If someone did, nothing is written and the command
  says to run it again, so no post or submission is lost.

Never edit or empty the ledger by hand to get past a refusal. If a record is wrong (a post that
was deleted before it went live), say so to the user and fix that one entry with them.

## proof.csv

The proof log is one file next to the ledger (`~/.ai-clipping/proof.csv`, or beside the file
`AI_CLIPPING_LEDGER` or `--ledger` names), for every campaign: each row names its campaign. So
`--proof` and `--earnings` give the same answer from any folder.

`ledger.py --proof analytics.json` reads the saved reply of WoopSocial's
`social_account_posts_list_analytics` (filter by account or project and a publish-date range) and
appends one row per post and collection: views, likes, comments, shares, engagement, when
WoopSocial collected the numbers and when the post went live. Posts that aren't in the ledger are
skipped; a second run with the same collection adds nothing. A reply saved as the MCP envelope
(`{"content": [{"type": "text", "text": "{...}"}]}`) is read too.

What the numbers are:

- WoopSocial collects them about once a day; reading doesn't refresh them. A daily snapshot, never
  real time.
- TikTok and YouTube views are plays. Instagram views are times shown, repeats included.
- The campaign's own tracker decides what is paid. Audience countries aren't in WoopSocial's
  per-post numbers: the user screenshots the app's analytics with countries.
- Two columns are the user's to fill: `submission_id` (also stored by `--submission-id`) and
  `us_share` (the share of viewers in the campaign's country, read from the screenshot, like
  `0.41`). Under the campaign's rule, `--earnings` says to expect a rejection. A proof.csv opened
  and saved in Excel is read as well.

## Evidence per post

Campaigns reject and dispute late; keep what proves each post. `submit.md` lists, per post, the
folder `proof/<post>/` (made by `--status`) and what goes in it:

- `submission.png`: the campaign's confirmation right after submitting, with the time.
- `48h-analytics.png`, `72h-analytics.png`, `7d-analytics.png`: the app's analytics at 48 hours,
  72 hours and 7 days after the post went live (plus any time the brief names), with views and
  audience countries.

Suggest a daily reminder while posts are inside their window: save the analytics reply, run
`--proof`, then `--earnings`.

## Earnings

`ledger.py --earnings` per campaign and post: the latest views inside the counting window, the
estimated payout (views / 1,000 x the platform's rate; nothing below that platform's minimum payout
or view minimum; at most its cap; minus the marketplace fee, 10% unless the campaign says
otherwise), days left in the window (from the day the clip crossed the payout threshold, as most
marketplaces count, or from posting when `window_from` is `"post"`), whether it was submitted, and engagement against the campaign's floor.

Say it straight: rates are about $1 per 1,000 views on Content Rewards (median), most clips get few
views, and budgets run out and campaigns pause. These are estimates. Never promise income, and
never suggest buying views, engagement groups or VPN tricks to lift a number: that is a permanent
ban.
