# Scaling notes

This doc covers performance characteristics and recommendations for running the skill against large ActiveCampaign accounts (100k+ contacts).

## What scales freely with account size

These reports are bounded by taxonomy or campaign count, not contact count. Run them on any account regardless of size:

- **Taxonomy reports**: `tag_audit`, `custom_field_audit`, `list_audit`, `segment_audit`, `automation_audit`, `automation_dependency_map`, `broken_automation_detector`, `form_audit`, `webhook_audit`, `pipeline_audit`
- **Campaign analysis**: `campaign_postmortem`, `subject_line_report`, `from_name_report`, `content_length_report`, `send_time_optimizer`, `send_frequency_report`, `monthly_performance`, `baseline_drift`, `campaign_velocity`, `link_performance`, `bounce_breakdown`
- **Single-contact operations**: `contact_data_export`
- **Account snapshots**: `account_archive`, `schema_diff`, `snapshot`
- **Headline numbers in `audit_list_health`** (uses `meta.total` rather than row scans)

Calibration is taxonomy-only and finishes in ~1 minute even on 1M-contact accounts.

## Contact-scanning reports and their default caps

| Script | Default cap | How to raise |
|---|---|---|
| `dedupe_contacts` | 10k | `--max-contacts N` |
| `role_address_finder` | 10k | `--max-contacts N` |
| `free_vs_corporate_report` | 10k | `--max-contacts N` |
| `contact_completeness_report` | 5k | `--max-contacts N` |
| `stale_contact_report` | 20k | edit script |
| `find_hot_leads` | 300 (post-filter) | API-side score filter; raise the constant if needed |

`audit_list_health`'s sampling pass accepts a configurable sample size for distribution math.

## Rate limits and runtime

The client throttles to **5 requests/sec** (`MAX_REQUESTS_PER_SEC` in `_ac_client.py`) — matches AC's default API limit on most plans. Pagination uses 100 records per page with a 250ms inter-page sleep, so the practical ceiling is ~4 pages/sec.

| Account size | Full scan runtime | API calls |
|---|---|---|
| 10k contacts | ~25 sec | 100 pages |
| 100k contacts | ~7 min | 1,000 pages |
| 500k contacts | ~35 min | 5,000 pages |
| 1M contacts | ~70 min | 10,000 pages |

These are best-case. AC may throttle harder on lower plans, and `offset` performance can degrade past ~100k records on some endpoints.

## Memory profile

`paginate()` accumulates the full result list before returning. `stream()` (added in 1.0.10) yields one record at a time — peak memory is bounded by the page size and whatever the caller keeps.

| Contact count | `paginate()` peak | `stream()` peak (single-pass aggregation) |
|---|---|---|
| 10k | 15–20 MB | <1 MB |
| 100k | 150–200 MB | <1 MB |
| 1M | 1.5–2 GB | <1 MB |

Scripts that already use `stream()`:

- `role_address_finder.py` — bounded by match count (typically <1k records).
- `free_vs_corporate_report.py` — bounded by unique-domain count (~thousands max).
- `stale_contact_report.py` — bounded by an activity-id-to-timestamp dict plus 50-record output samples; total under 50 MB even on 1M-contact accounts.
- `dedupe_contacts.py` (1.0.11) — slim records (id + email only) keyed by email/phone/name. Singletons sit in lookup maps until promoted to the duplicate output; full records never accumulate. Peak ~150 MB on 1M-contact accounts vs. 1.5–2 GB before.

### Scripts intentionally still buffered

- **`audit_list_health.py`** already operates on a `sample_size`-bounded subset by design — it computes distribution math, not per-contact records. Streaming would shave ~150 MB at most; not worth the refactor.
- **`contact_completeness_report.py`** joins contacts with their field values. Both sets must be in memory together to do the join. Streaming the contact side would force a per-contact `/contacts/{id}/fieldValues` API call — at 5 req/sec, a 100k-contact join would take ~5.5 hours instead of ~30 sec. The memory savings aren't worth a 600× slowdown. If you have a bigger account and need this report, scope it to a list or tag first.

## Recommended workflows for large accounts

**1. Run taxonomy-bound reports freely.** Tag audits, automation hygiene, segment audits, campaign analysis — all unaffected by contact count.

**2. Scope contact-scanning reports to cohorts.** Instead of running `dedupe_contacts` against the full account, run it on a single list. Most marketing questions are naturally cohort-scoped.

**3. For one-shot full scans, plan for runtime.** Full taxonomy archives: bump `--max-contacts`, run overnight, expect ~1 hour per 150k contacts.

**4. Use snapshots for change detection.** `account_archive.py` + `schema_diff.py` are taxonomy-only and weekly-cron-friendly even for huge accounts.

## What's not optimized yet

- **Parallel cohort scans**: pagination is serial per script. Could be parallelized with rate-aware backoff. Useful for workflows like "list health on each of 13 lists" — sequential today, parallel would be ~5× faster.
- **Offset performance**: AC's `offset` parameter slows past ~100k records on some endpoints. Cursor-based pagination (`orders[id]=ASC&id_greater=N`) is supported on some endpoints — see `references/contacts.md`.

If your account is in the 500k+ range and any of these matter for your workflow, please file an issue at https://github.com/ji282h7/activecampaign-claw/issues.
