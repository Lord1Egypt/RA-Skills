## Description:

CSV Tools helps agents inspect, clean, transform, validate, profile, sample, split, merge, and summarize CSV or TSV files using a local Python standard-library script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to have an agent run local CSV or TSV inspection, cleaning, validation, profiling, sampling, splitting, merging, and column-transformation workflows before import, ETL, or data-quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands that write CSV outputs may overwrite existing files or create default output files in the working directory.

Mitigation: Run the skill in a scratch directory when possible, pass explicit --output paths, and inspect destination paths before execution.

Risk: Untrusted CSV content can remain risky if generated outputs are later opened in spreadsheet software.

Mitigation: Treat untrusted CSVs as data only and review or sanitize formula-like fields before opening generated files in spreadsheet tools.

Risk: The artifact documentation overstates confirmation controls for writes.

Mitigation: Do not rely on interactive overwrite confirmation; keep original inputs read-only or backed up and review generated files before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cqdev-ai/skills/csv-tools)
- [Publisher Profile](https://clawhub.ai/user/cqdev-ai)
- [Artifact README](artifact/README.md)
- [Artifact Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands; command results may be terminal text, CSV files, or JSON validation reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on explicit CSV or TSV paths; use explicit output paths for commands that write files.]

## Skill Version(s):

1.1.0 (source: server release metadata, CHANGELOG, package.json; released 2026-07-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
