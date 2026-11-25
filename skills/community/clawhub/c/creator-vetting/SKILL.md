---
name: creator-vetting
description: Vet an Instagram creator before paying them for a collaboration - real engagement vs follower count, consistency, reel performance, suspicious spikes, past brand deals and audience-fit signals - with a clear go / caution / skip verdict, using SocialAPIs. Use when the user is choosing influencers, checking a creator's media-kit claims, comparing a shortlist of creators, or worried about fake followers.
---

# Creator vetting

Before a brand pays a creator, check the public numbers behind the media kit. This skill produces a verdict with the evidence, not a vanity summary.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `instagram_profile`.

## Ask first (only what's missing)

- Instagram username(s), up to about 10.
- The brand / product and target audience (country, interests), so fit can be judged.
- Any claims to verify ("40k average reel views").

## Budget

Per creator about 5 to 8 credits: profile 1, user id 1, posts 2 to 3 pages, reels 1 to 2 pages, optionally highlights 1. Ten creators is about 60 to 80 credits; agree on it first.

## Steps

1. `/instagram/profile/details?username=…`: followers, following, posts count, verified, bio, external link, related profiles.
2. `/instagram/profile/posts?username=…`: the last 24 to 36 posts (follow `end_cursor`): likes, comments, caption, timestamp, type.
3. `/instagram/user/id?username=…`, then `/instagram/profile/reels?user_id=<long user_id>` for the last 12 to 24 reels with play counts.
4. Optional: `/instagram/profile/highlights?user_id=<pk>` to see if they keep "collabs" / "reviews" highlights (proof of past brand work).

## What to compute

- **Engagement rate** = median (likes + comments) of the last posts / followers. Rough norms on Instagram: under 10k followers 3-6% is healthy; 10k to 100k 1.5-3.5%; 100k to 1M 1-2.5%; above 1M under 1.5% is normal. Very low for the size is a warning; very high can be a pod.
- **Comments to likes ratio**: under 0.5% suggests passive or bought likes; scan comment counts on the top posts.
- **Consistency**: posts per week, gaps over 3 weeks, and the spread of engagement (median vs average: a huge gap means a few viral posts carry the average).
- **Reel reach**: median plays vs followers. Median plays under ~5% of followers on an account that mostly posts reels is weak.
- **Spikes**: a post or reel 10x the median with no obvious reason (giveaway, trending audio, collab) is worth asking about.
- **Past brand deals**: captions with #ad, #sponsored, #partner, "paid partnership", "use my code", "gifted", tagged brands. List the brands; competitors of the user's brand matter.
- **Audience-fit signals**: caption language, locations tagged, the kind of related profiles, topics. Signals, not demographics; say so.

## Verdict

- **Go**: engagement in or above the band, steady posting, no unexplained spikes, relevant content, past deals look normal.
- **Caution**: one or two weak signals (low reel reach, recent follower jump, many giveaways, works with a direct competitor). Say what to ask for: screenshots of Stories reach and audience country from their Insights.
- **Skip**: engagement far below the band, comments generic or near zero, posting abandoned, or content that conflicts with the brand.

## Output

```
## Creator check: @<username>, <date>   Verdict: GO / CAUTION / SKIP

| Followers | Eng. rate (median) | Band for size | Posts/wk | Reel median plays | Plays / followers |
|---|---|---|---|---|---|

Evidence
- …
Past brand work: <brands, dates, links>
Ask the creator for: <specific Insights screenshots, rates for reel + stories>
```

For a shortlist, add a ranking table with one row per creator and the verdict column first.

## Limits and fairness

- Public counts only: no audience demographics, Stories views or saves. Those come from the creator's own Insights; tell the user to request them.
- Don't label someone a fraud. Report numbers and say "worth checking".
- Instagram comments aren't available through the API, so comment quality is judged from counts and captions only.
