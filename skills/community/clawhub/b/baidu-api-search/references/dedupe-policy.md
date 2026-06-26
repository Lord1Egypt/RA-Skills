# Dedupe Policy

Use this reference before changing dedupe behavior.

## Principle

Deduplication must not destroy evidence. Keep raw results and write duplicate mappings.

## URL Canonicalization

Normalize:

```text
scheme
host case
mobile host prefix m.
trailing slash
tracking params such as utm_*, from, spm, share, source
fragment removal
```

Keep:

```text
original_url
canonical_url
query
rank
```

## Title and Summary Similarity

Clean text by:

```text
lower/casefold
remove whitespace and punctuation noise
remove common source suffixes
```

Default thresholds:

```text
title_similarity >= 0.92
summary_similarity >= 0.94
```

These thresholds are conservative for v1. If they remove too much, lower their influence or mark near-duplicates without dropping them from selected sources.

## Quality Flags

Current v1 flags:

```text
possible_ad_or_low_quality
deep_subdomain
missing_url
domain_limit_overflow
```

Do not treat these as final truth. They are signals for ranking and human/agent review.

## Domain Distribution

Default `--domain-limit 8` flags overflow from a single domain. It does not delete the source by default.

Official, primary, or high-authority domains may deserve a higher cap. SEO aggregators and mirrors should receive lower priority.

