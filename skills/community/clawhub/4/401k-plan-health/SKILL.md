# Research a Company's 401(k) Plan Health

Look up Form 5500-derived data on a specific company's retirement plan(s) using planprovider.pro. Use this to evaluate plan health, benchmark against peers, surface red flags, or prepare for a sales / consulting conversation.

## When to use this skill

Use when the user asks to:

- Look up a company's 401(k), 403(b), or retirement plan
- Evaluate plan health (fees, participation, investment menu, compliance signals)
- See which TPA / recordkeeper / advisor / auditor a company currently uses
- Benchmark a plan against industry / size peers
- Prepare for a meeting with a plan sponsor

## Data source

planprovider.pro maintains a company directory built from DOL Form 5500 filings. Each company page lists current providers, plan stats, and historical filings. Markdown is available via content negotiation:

```
GET https://planprovider.pro/<path>
Accept: text/markdown
```

### Useful URLs

- `https://planprovider.pro/companies` — company index
- `https://planprovider.pro/companies/{state-slug}` — companies by state
- `https://planprovider.pro/companies/{slug}` — individual company plan profile (plan name, EIN, participants, total assets, current TPA / recordkeeper / advisor / auditor, recent filings, plan type)

## Recommended workflow

1. **Identify the company.** Get the company name and (if possible) state or EIN. Fetch `/companies` or `/companies/{state}` and search by name, or guess the slug pattern (`/companies/{kebab-case-name}`) and try fetching directly.
2. **Pull the plan profile.** Fetch `/companies/{slug}` as markdown. Extract: plan name(s), participants, total assets, plan type, current providers (TPA, recordkeeper, advisor, auditor), and any historical changes.
3. **Surface health signals.** From the markdown, comment on:
   - **Scale fit** — are the current providers' typical client sizes a match?
   - **Audit status** — is the plan large enough to require an audit, and is an auditor listed?
   - **Provider tenure / changes** — recent provider switches can indicate dissatisfaction or a recent RFP.
   - **Plan type complexity** — DB, cash balance, ESOP, or MEP add specialist requirements.
4. **Optional benchmarking.** Cross-reference with `/benchmarks/...` skill (research-401k-benchmarks) to compare the plan's stats to industry averages.
5. **Hand off.** Return a structured summary: company name, plan size, current providers (with profile links), notable signals, and the source URL.

## Important constraints

- Only report data that appears in the planprovider.pro markdown response. Do **not** invent EINs, balances, or provider relationships.
- Form 5500 data lags by ~12–18 months; flag the filing year shown on the page as the "as-of" date.
- This is **public DOL data** — using it for research is appropriate; respect any usage notes in the page footer.
- If a company is not found, do not fabricate a profile — report "not currently in the planprovider.pro directory" and offer to search by EIN or alternate name.

## Output format

A markdown summary with: **Company**, plan name, EIN (if shown), participants, total assets, plan type, list of current providers (each linked to its `/provider/{slug}` page), notable health signals, and the source company URL.
