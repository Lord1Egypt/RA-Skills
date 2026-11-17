## Description:

Formats supported citation inputs into AMA-style references for academic and journal-submission workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, editors, and developers use this skill to convert supported citation strings or local citation files into AMA-style formatted references. It is useful for preparing academic manuscripts when outputs will still receive human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package documentation materially overstates capabilities beyond the local AMA citation formatter.

Mitigation: Treat the skill as a supported-input AMA formatter and manually verify journal-specific requirements; do not rely on advertised 1000+ styles, validation, bibliography generation, or reference-manager integration unless those features are added and tested.

Risk: Batch mode can overwrite a chosen output file.

Mitigation: Use a new output path or back up existing files before running batch formatting.

## Reference(s):

- [AMA Citation Style Guide](artifact/references/ama-guidelines.md)
- [Example Citations for Testing](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text citations, Markdown responses, and optional text files for batch output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode writes formatted citations to the user-provided output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
