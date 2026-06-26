# Official Doc Sources

## Purpose
This file defines which official MiniMax sources this skill should verify periodically.

## Sources to check

### 1. Token Plan FAQ
- URL: `https://platform.minimaxi.com/docs/token-plan/faq`
- Why: quota reset rules, supported model families, usage restrictions, dynamic throttling, weekly limits

### 2. Token Plan remains API
- URL: `https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains`
- Why: real-time quota buckets, current interval usage, weekly usage fields

## What to compare against local references

### `references/api_info.md`
Check:
- model family names
- flagship vs alternative models
- request-unit notes

### `references/costs.json`
Check:
- request estimates per model
- default plan assumptions
- rolling window assumptions

### `references/quota_mapping.json`
Check:
- runtime model ids ↔ official quota bucket names
- reset rules (`rolling-5h` vs `daily`)

## Verification principle
The checker should not auto-edit production references. It should produce a difference report for human review.
