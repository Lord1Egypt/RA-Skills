# Markdown Export Policy

The canonical export format for this skill is Markdown.

## Default Export Root

When the user asks to export, save reports under:

```text
reports/earbuds/
```

All Bluetooth earbuds reports should be grouped in this single folder unless the user explicitly asks for another path.

## Filename Convention

Use this filename shape:

```text
YYYY-MM-DD-earbuds-<region>-<budget-or-brand>-<use-case>.md
```

Examples:

```text
reports/earbuds/2026-05-08-earbuds-china-under-1000-cny-commuting-calls.md
reports/earbuds/2026-05-08-earbuds-china-sony-1000-1800-cny-anc-calls.md
reports/earbuds/2026-05-08-earbuds-us-iphone-premium-anc.md
```

## Title Convention

The first line of the Markdown file should be a meaningful H1 title:

```markdown
# Bluetooth Earbuds Buying Report: China, Under 1000 CNY, Commuting + Calls
```

For brand-scoped reports:

```markdown
# Sony Bluetooth Earbuds Buying Report: China, 1000-1800 CNY, ANC + Calls
```

## Required Metadata Block

After the title, include a short metadata block:

```markdown
- Generated: YYYY-MM-DD
- Region: China
- Currency: CNY
- Budget: Under 1000 CNY
- Brand scope: Open market
- Use case: Commuting, calls
- Product links: Included when available
- Confidence: Medium
```

## Export Behavior

When the user requests export:

1. Generate the report normally using `templates/report-template.md`.
2. Choose a clear title using region, budget/brand, and primary use case.
3. Save the report as a Markdown file under `reports/earbuds/`.
4. Include direct product links or clearly labeled marketplace search links when available.
5. Tell the user the exact saved path.
6. If a file with the same name exists, append `-v2`, `-v3`, etc. rather than overwriting unless the user asks to overwrite.

## Path Safety

- Use lowercase, hyphenated filenames.
- Remove punctuation from filename parts.
- Keep filenames readable, not overly long.
- Do not include private user identifiers in filenames.
- Use the user's requested folder if explicitly provided.
