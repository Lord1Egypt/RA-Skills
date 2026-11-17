## Description:

Query Australian Bureau of Statistics (ABS) datasets via natural language and return data with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billybodean](https://clawhub.ai/user/billybodean)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to find and query ABS time-series datasets, compare Australian economic indicators, and return sourced tables, summaries, JSON, CSV, or charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls the public ABS API and creates a local metadata cache in ~/.cache/abs-data-api.

Mitigation: Install it only when an Australia/ABS-specific data helper is needed, and expect public API calls plus cached public metadata.

Risk: User-requested --out or --chart operations can write files and may overwrite existing paths.

Mitigation: Choose output paths deliberately and review generated file locations before running write-producing commands.

Risk: Broad queries, especially all-dimension requests, may return large or hard-to-interpret result sets.

Mitigation: Prefer validated presets, --latest, date ranges, or structure inspection before broad direct queries.

## Reference(s):

- [ABS Data API - Quick Reference Guide](artifact/references/api-guide.md)
- [ABS Data API - Dataset Catalog](artifact/references/dataset-catalog.md)
- [ABS SDMX Dimension Patterns](artifact/references/sdmx-patterns.md)
- [ABS Data API base endpoint](https://data.api.abs.gov.au/rest)
- [ABS dataflow endpoint](https://data.api.abs.gov.au/rest/dataflow/ABS)
- [ClawHub skill page](https://clawhub.ai/billybodean/skills/abs-data-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, text, CSV, JSON, and PNG chart outputs with ABS citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write user-requested output files with --out or --chart; chart output requires matplotlib and falls back to text when unavailable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
