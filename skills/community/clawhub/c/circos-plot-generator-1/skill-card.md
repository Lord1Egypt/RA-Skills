## Description:

Use blind-review-sanitizer for academic writing workflows that need structured anonymization, explicit assumptions, and clear output boundaries for double-blind submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and academic writers use this skill to prepare manuscripts for double-blind review by removing or highlighting likely author-identifying content and returning bounded review notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removed identifiers may appear in terminal output or logs.

Mitigation: Run in a private workspace and prefer counts-only summaries before processing sensitive manuscripts.

Risk: Generated output can overwrite existing files when an explicit output path is reused.

Mitigation: Process copies of manuscripts and review output paths before execution.

Risk: DOCX processing depends on an inconsistent unpinned dependency declaration.

Mitigation: Review and pin the DOCX dependency before installation, or limit use to supported text and Markdown files.

Risk: Automated anonymization may miss metadata, figures, headers, footers, supplementary files, or some acknowledgment content.

Mitigation: Require final human review of all manuscript surfaces before double-blind submission.

Risk: Release metadata names Circos Plot Generator while artifact behavior describes blind-review-sanitizer.

Mitigation: Confirm the release title and artifact package match before publishing the public Skill Card.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/circos-plot-generator-1)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown guidance with optional generated manuscript files and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create blinded manuscript copies and summarize removed identifiers or remaining manual review items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
