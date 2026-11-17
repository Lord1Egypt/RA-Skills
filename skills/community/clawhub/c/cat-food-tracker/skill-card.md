## Description:

Work with cat feeding, weight, and water tracking records. Use when validating CatFoodCalculator-style JSON backups, calculating dry-equivalent cat food totals, estimating water intake from wet food, summarizing pet feeding records by day, converting summaries to CSV, or helping users clean up offline pet feeding data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhr8](https://clawhub.ai/user/hhr8)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to validate offline cat feeding backups, calculate daily food, water, and weight summaries, and export normalized summaries to JSON or CSV. It supports data cleanup and reporting for CatFoodCalculator-style records, not veterinary recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cat names and feeding histories can reveal private user data.

Mitigation: Treat backup contents as private and avoid including real pet names, feeding records, or backup files in examples, logs, commits, or published packages unless the user explicitly requests it.

Risk: Generated CSV output may be unsafe to open directly in spreadsheet software until formula neutralization is added.

Mitigation: Use trusted backup files for CSV export and review or neutralize formula-like cell values before opening generated CSVs in spreadsheet applications.

Risk: Very large untrusted inputs can consume memory before size rejection occurs.

Mitigation: Precheck backup file sizes and avoid piping or loading very large untrusted files.

## Reference(s):

- [Domain Model](references/domain-model.md)
- [Calculations](references/calculations.md)
- [Import And Export](references/import-export.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON validation reports, and CSV or JSON daily summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local CatFoodCalculator-style JSON backups and may emit warnings for unsupported fields or missing pet references.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
