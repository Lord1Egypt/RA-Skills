# SEO Link Building Standard (AI SBTI Skill Test)

## Objective

Build sustainable off-page authority for `https://aisbti.com/` and transfer that authority to priority internal URLs through controlled internal linking.

## Hard Requirements

- Keep links relevant to personality testing, psychology topics, education, or closely related niches.
- Prefer indexed pages with stable crawlability.
- Prioritize dofollow editorial placements.
- Reject links from hacked, malware, adult, gambling, or obvious spam domains.
- Maintain gradual acquisition pace to avoid unnatural spikes.

## Source Quality Threshold

Minimum acceptance gates before outreach effort:

- `relevance >= 0.60`
- `authority >= 45`
- `indexed == 1`
- `outbound_links <= 180`

For high-priority campaigns, use stricter gates:

- `relevance >= 0.75`
- `authority >= 60`
- `placement in {editorial, guest-post, directory}`

## Anchor Distribution Guardrails

Monthly target distribution:

- Branded anchors: 45% to 60%
- URL anchors: 15% to 25%
- Partial-match anchors: 15% to 25%
- Exact-match anchors: <= 10%

If exact-match exceeds 10%, deprioritize exact-match opportunities in next run.

## Landing Page Distribution

Do not send most links to homepage only.

Recommended distribution:

- Homepage: <= 25%
- Core explanation pages: 35% to 45%
- Comparison or long-tail pages: 30% to 40%

## Weight Relay Rules

After an external link lands on `landing_url`, add contextual internal links from that page to conversion pages:

- Keep relay link depth <= 2 clicks from homepage.
- Use descriptive anchors, not repetitive exact keywords.
- Relay ratio baseline: 0.20 to 0.40 per internal target.
- Prefer 2 to 4 relay targets per high-value landing page.

## Cadence

- Start phase: 5 to 12 acquired links per week.
- Growth phase: 10 to 20 acquired links per week.
- Keep `dofollow:nofollow` around `70:30` to `85:15`.

## QA Checklist

- Link is live and indexable.
- Final destination URL is canonical and returns `200`.
- Anchor category is within distribution guardrails.
- Link placement is contextual, not hidden.
- Opportunity and outcome recorded in planning JSON.
