---
name: crowdfunding-campaign-research
description: Compare Kickstarter campaigns through Crawlora using funding snapshots, reward tiers, creator updates, risks, and sampled backer comments. Use for campaign benchmarks, launch research, or evidence-based progress and fulfillment briefs.
---

# Crowdfunding campaign research

Compare campaigns with their currencies, lifecycle stages, and evidence limits
intact. Funding success, creator statements, and fulfilled rewards are distinct.

## Setup

Set `CRAWLORA_API_KEY` to your key from [crawlora.net](https://crawlora.net).
Run the bundled `scripts/crawlora.sh` from this skill directory or by absolute
path. It sends `x-api-key` to `https://api.crawlora.net/api/v1`; keep the key in
the environment. Read [reference/endpoints.md](reference/endpoints.md) for the
four Kickstarter tools and optional public page research.

## Discover and inspect campaigns

1. Define the product category, comparison purpose, campaign stage, and collection
   bound. Search `/kickstarter/discover` with `term`, 1-based `page`, and `sort`:
   `magic`, `popularity`, `newest`, `end_date`, or `most_funded`.
2. Set `state` explicitly for a lifecycle comparison. Repeat the key for multiple
   values: `upcoming`, `live`, `late_pledge`, `canceled`, `failed`, `successful`.
   Omitted state uses the upstream live/late-pledge default, which cannot establish
   historical success rates. `staff_pick_only` introduces editorial selection.
   Use returned `category.id` for a narrower query; there is no dedicated category
   discovery endpoint in this selection, so do not invent category IDs.
3. Resolve the canonical project URL. Extract BOTH its creator path segment and
   project slug for `/kickstarter/project`, `/kickstarter/updates`, and
   `/kickstarter/comments`. Creator display names and numeric IDs are not substitutes.
4. Compare goal, pledged amount, backer count, lifecycle state, launch/deadline,
   and collection time. Match currency or use an explicitly labeled comparable
   conversion. Funding percent is not a comparable scale of absolute demand;
   different goals and elapsed campaign durations matter.
5. Inspect story, risks, and available reward tiers. Preserve amounts, currencies,
   shipping conditions, estimated delivery, and availability. Missing `reward_tiers`
   can mean capture failure or no tiers. Project goal/percent/date fields may be
   zero when a supplemental lookup misses; cross-check discovery before calculating
   ratios or interpreting a zero as a genuine campaign value.
6. Read creator updates in chronological context, distinguishing promises,
   reported production/shipping milestones, and independently supported outcomes.
   The updates endpoint has no page parameter; preserve the returned coverage.
7. Sample comments with explicit limits: the comments endpoint exposes only the
   initial batch, without further pagination. `total_count` is the feed's total,
   not the number collected. Exclude `is_creator=true` replies from backer-comment
   denominators. Attribute concerns as reports, not established defects or fraud.

```sh
scripts/crawlora.sh /kickstarter/discover \
  term="board game" state=live state=successful sort=newest page=1
# Read creator and slug from a returned /projects/CREATOR/SLUG URL.
```

## Deliverable and interpretation

Return campaign links, cohort rules, dated funding/reward comparisons, update
milestones, sampled comment themes with counts, disagreements, and open questions.
For a single snapshot, describe status; do not invent funding velocity or earlier
daily totals. State how many comments were collected versus the reported total.

- Successful funding is not proof of reward delivery or profitable production.
  See [Kickstarter's project basics](https://help.kickstarter.com/hc/en-us/articles/115005028514-What-are-the-basics).
- A self-selected set of highly funded projects cannot estimate platform success
  rates. Average pledge size is not necessarily a unit price or units sold.
- Keep update date strings when parsing is ambiguous and cite short excerpts.
  Research does not pledge, message creators, or create recurring monitoring.
- Bound discovery pages and detail calls. Stop on empty/repeated pages. Back off
  on `429`, retry transient `5xx` once, stop on `401`/`403`, and check application
  `code`; missing sources should remain visible in the resulting brief.
