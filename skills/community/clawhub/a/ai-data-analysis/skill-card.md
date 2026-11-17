## Description:

Provides local CSV analysis and data-cleaning utilities that generate markdown reports or cleaned CSV/JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthasking123](https://clawhub.ai/user/arthasking123)

### License/Terms of Use:

MIT

## Use Case:

Developers, data analysts, and operations teams use this skill to run local CSV summary analysis and basic cleaning, then save markdown reports or cleaned CSV/JSON files for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation describes Excel, charts, PDF/HTML export, trend detection, anomaly detection, and prediction, but security evidence identifies the implemented behavior as a basic CSV-only local analysis and cleaning utility.

Mitigation: Treat the release as CSV-only unless updated evidence proves additional formats or report types are implemented.

Risk: The skill writes generated report or cleaned-data files into its local output directory.

Mitigation: Run it only on data intended for local analysis and review generated files before sharing or relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arthasking123/skills/ai-data-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration]

**Output Format:** [Markdown reports, CSV files, JSON files, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated reports and cleaned data into a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, SKILL.md, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
