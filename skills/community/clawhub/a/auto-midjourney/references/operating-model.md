# Operating Model

Use this skill as a personal assistant for Midjourney Alpha web, not as a bulk automation framework.

## Recommended workflow

1. Run `python3 scripts/mj_doctor.py --fetch-user-state`
2. Confirm inferred `user_id` and `channel_id`
3. Build or refine the prompt with `python3 scripts/mj_prompt_helper.py ...` when the user needs template-based help
4. Submit one prompt with `python3 scripts/run_imagine.py "<prompt>" --sync-user-state`
5. Keep the built-in spacing enabled, but tune it pragmatically for real usage
6. Use `python3 scripts/run_imagine.py "<prompt>" --sync-user-state --wait-page-assets --download --convert-to png` when you need a verified local result
7. Use `python3 scripts/list_recent_jobs.py --amount 10` to inspect recent jobs

The preferred browser verification path now watches the existing Midjourney tab's network responses for matching `job_id` image URLs. This is quieter than forcing repeated page refreshes or navigation.

## Why this model is safer

- fewer manual header mistakes
- fewer duplicate submits
- avoids bursty request patterns
- easier to keep one human action mapped to one live submit

## Do not do this

- long unattended loops
- multi-account rotation
- burst retries to “push through” failures
- scraping or background polling at high frequency

## Local throttling defaults

The current defaults are intentionally light-weight:

- minimum interval: 3 seconds
- hourly cap: disabled by default
- daily cap: disabled by default

These are local tool limits, not official Midjourney limits. If you want stricter guardrails, set the hourly and daily caps explicitly in `.env`.

## Batch workflow

When you need multiple prompts, use `scripts/batch_generate.py` with a plain text prompts file. It can submit a small batch first, then wait for that batch to resolve, and can pause between batches with `--batch-size` plus `--batch-cooldown-seconds`.
