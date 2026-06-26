# Recipe: Pre-import checklist

What to run before importing a contact CSV into ActiveCampaign — so you don't waste contact-tier slots on bad addresses or pollute your sender reputation.

## When to use this

- "I'm about to import [N] contacts from [source]."
- "Got a list from a partner / event / sales — should I import it?"
- "Cleaning up an old export before re-importing."
- After exporting from another ESP during a migration.

## What it produces

1. **Validation report** — bad emails, duplicates, role addresses, free-vs-corporate composition.
2. **Plan-impact estimate** — how many net-new contacts this will add (vs. matching existing).
3. **Risk flags** — anything that could hurt deliverability if imported as-is.
4. **Recommended actions** — what to remove or split before the import.

## How the agent runs it

The pre-import flow is **local-only** until the user explicitly approves the import. Nothing touches AC until the validation passes.

1. `python3 {baseDir}/scripts/import_validator.py <csv-path>` — local CSV scan: malformed emails, duplicates within the file, role addresses, free-vs-corporate split. **No AC API calls.**
2. If the user wants to estimate plan impact, the agent samples a few emails from the CSV and queries AC to see how many already exist. (Don't query everything — that wastes API budget; sample 50 and extrapolate.)
3. If a sender domain or list source is involved, run `python3 {baseDir}/scripts/role_address_finder.py` against the existing list to see if the same role-address patterns are already a problem.
4. Synthesize the verdict: clean, conditional, or do-not-import.

## Validation thresholds

| Check | Pass | Conditional | Do-not-import |
|---|---|---|---|
| Malformed emails | <1% | 1–5% | >5% (CSV is corrupt or scraped) |
| In-file duplicates | <2% | 2–5% | >5% (deduplicate first) |
| Role addresses | <2% | 2–5% | >5% (scraped lead list) |
| Free-mail share | varies | — | >90% with no enrichment (consumer list with no segmentation) |
| Already-in-AC overlap | <30% | 30–70% | — (high overlap is fine — just net-new is small) |

## Sample report output

```
# Pre-Import Check — leads-q2-2026.csv

File: leads-q2-2026.csv (3,847 rows)
Email column: detected as "Email"

## Headline numbers
- Total rows: 3,847
- Valid emails: 3,712 (96.5%)
- Blank emails: 18
- Malformed: 117 (3.0%)

## Role addresses (3.2%)
- 124 detected: info@, support@, noreply@, sales@, contact@
- ❗ List source likely scraped or imported from a public directory.

## Duplicates within file: 96 (2.5%)
- Case-insensitive duplicates (Alice@Acme.com + alice@acme.com): 67
- Whitespace duplicates: 14
- Exact duplicates: 15

## Composition
- Free mail: 2,103 (56%)
- Corporate: 1,609 (44%)
- Top domains: gmail.com (32%), outlook.com (12%), acmecorp.com (4%)

## Plan impact (sampled)
- Sampled 50 emails; 38% already in AC (likely 1,400 net-new of 3,712 valid).

## Verdict: CONDITIONAL

Risks:
- 3.2% role address share is borderline — these will hurt engagement and may trigger spam traps.
- 56% free-mail share is fine for B2C; concerning for B2B segmentation.

Required cleanups before import:
1. Remove the 124 role addresses (info@, support@, etc.)
2. Deduplicate to lowercase canonical (96 rows)
3. Drop the 117 malformed rows

Optional improvements:
4. If this is a B2B list, append company data before import — 56% free-mail share without enrichment will be hard to segment.
5. Tag the import batch with `import-2026-04-leads-q2` so you can track engagement of this cohort separately.
```

## Customization parameters

| Parameter | Default | Notes |
|---|---|---|
| `--email-column` | auto-detect | Specify if the CSV has multiple email-like columns. |
| `--max-malformed` | 5% | Threshold for do-not-import. |
| `--max-roles` | 5% | Same. |
| `--sample-size` | 50 | For plan-impact estimation. Bump for higher confidence on small files. |

## Action follow-ups

After the user reviews the report, the agent should ask:

1. **If verdict is PASS:** "Want me to draft an AC import config (list to import to, tags to apply, source field) so you have everything ready?"
2. **If verdict is CONDITIONAL:** "Should I generate a cleaned CSV with the flagged rows removed? I'll show you the diff before writing."
3. **If verdict is DO-NOT-IMPORT:** "This looks like a [scraped / very dirty / non-opt-in] list. Importing it will hurt your sender reputation — sending to scraped role addresses is the #1 cause of spam-trap hits. Want to discuss alternatives (re-collecting consent via a sign-up form, a double opt-in confirmation flow, or running a re-engagement campaign on contacts you already have permission to email)?"

## Outcome logging

```jsonl
{"ts":"...","action":"recipe_executed","recipe":"pre-import-checklist","file":"leads-q2-2026.csv","total_rows":3847,"verdict":"conditional","action_count":3}
```

## What this recipe will NOT do

- **Will not import the file.** AC's CSV import is done in the AC UI; this recipe produces validation only.
- **Will not call email-validation services** (NeverBounce, ZeroBounce, etc.). The pattern-level checks here catch ~80% of bad addresses for free; deeper validation requires a paid service.
- **Will not enrich the data.** Free-vs-corporate split is structural only. For real B2B enrichment, hand the cleaned CSV to your enrichment tool of choice before AC import.

## Related

- `scripts/import_validator.py` — the local CSV scanner.
- `scripts/role_address_finder.py` — also checks already-in-AC contacts for the same patterns.
- `recipes/list-health-audit.md` — what to run AFTER an import to verify it didn't degrade list health.
- `frameworks/email-best-practices.md` — deliverability principles.
