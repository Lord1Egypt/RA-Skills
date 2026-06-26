# Ranking model

Use this ranking model to order candidate stories before selecting the top 10.

## Signals

- **Freshness**: how recently the story was published
- **Source reputation**: how trustworthy and authoritative the source is
- **Coverage**: how many independent credible sources cover the same story
- **Engagement**: trend velocity from community signals such as HN points, Reddit activity, or GitHub momentum

## Default weights

```text
score =
  freshness * 0.35 +
  source_reputation * 0.30 +
  coverage * 0.20 +
  engagement * 0.15
```

## Suggested scoring hints

### Freshness

- 100: published within 6 hours
- 80: published within 24 hours
- 60: published within 3 days
- 40: published within 7 days
- 20: older than 7 days but still relevant

### Source reputation

- 100: official company or lab announcement
- 90: Reuters or other highly trusted wire service
- 85: top-tier editorial tech publication
- 75: respected technical blog or research lab
- 60: community source or niche publication
- 40 or below: weak or unverified source

### Coverage

- 100: 3 or more strong independent sources
- 80: 2 strong independent sources
- 60: 1 strong source plus a community signal
- 30: single source only

### Engagement

- 100: clear spike across multiple community sources
- 70: notable HN / GitHub / Reddit momentum
- 40: modest discussion
- 10: little or no engagement signal

## Tie-breakers

When two stories score similarly, prefer the story that is:

1. More recent
2. Supported by stronger sources
3. More directly about a material AI release or breakthrough
4. Less redundant with other items in the list

## Topic-specific adjustments

- **Research briefing**: increase coverage and source reputation, decrease community engagement
- **Startup/product briefing**: increase freshness and engagement
- **Enterprise briefing**: increase source reputation and editorial coverage
- **Consumer briefing**: increase editorial coverage and social momentum
