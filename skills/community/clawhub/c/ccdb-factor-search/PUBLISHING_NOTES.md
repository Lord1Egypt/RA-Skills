# Publishing Notes

## Intended use

This skill is for CCDB / Carbonstop carbon-factor lookup where the user needs the most suitable factor, not just a raw result list.

## Differentiators

- extracts search intent from natural-language requests
- searches in both Chinese and English
- iteratively refines search terms
- compares candidates across multiple rounds
- downgrades unsuitable factors (wrong region, wrong unit, spend-based mismatch, etc.)
- returns a reasoned recommendation with risks and alternatives

## Runtime dependency

This skill depends on access to the Carbonstop CCDB API.

Current default endpoint:
- `https://gateway.carbonstop.com/management/system/website/queryFactorListClaw`

The endpoint can still be overridden with `CCDB_API_BASE_URL` when needed.

## Environment variables

- `CCDB_API_BASE_URL` (optional; defaults to the production endpoint above)
- `CCDB_SIGN_PREFIX` (optional; defaults to `openclaw_ccdb`)

## Pre-publish checklist

- confirm production API endpoint
- confirm rate limits / auth behavior
- verify 5+ representative evals
- review term lexicon with domain experts
- confirm output wording is suitable for end users

## Suggested publish summary

A CCDB carbon-factor matching skill for Carbonstop APIs. It extracts keywords from user requests, searches both Chinese and English terms, iteratively refines search keywords, ranks candidates, rejects unsuitable matches, and returns the best-fit emission factor with reasoning and risk notes.
