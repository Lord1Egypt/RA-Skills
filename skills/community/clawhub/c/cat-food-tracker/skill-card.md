## Description: <br>
Processes CatFoodCalculator-style cat feeding, weight, and water records for validation, dry-equivalent food totals, water estimates, daily summaries, CSV export, and offline data cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhr8](https://clawhub.ai/user/hhr8) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to validate private cat feeding backups, calculate daily food, water, and weight summaries, export CSV, and normalize offline records without making veterinary recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan marked the release suspicious because developer tooling may run local commands or interact with external services with broad local access. <br>
Mitigation: Install only if you trust the publisher, review commands before execution, and disable sandbox or approval bypass behavior unless full local access is intentional. <br>
Risk: Cat names, feeding history, weight records, and water records may be private user data in backups and generated summaries. <br>
Mitigation: Keep real backups and pet names out of examples, logs, commits, and published packages unless the user explicitly requests sharing. <br>


## Reference(s): <br>
- [Calculations](references/calculations.md) <br>
- [Domain Model](references/domain-model.md) <br>
- [Import And Export](references/import-export.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; bundled scripts emit JSON or CSV reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validates CatFoodCalculator-style JSON backups up to 5 MB; summaries can be filtered by pet and date range.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
