## Description:

Produces an investment-banker-grade research memo and data provenance table from Chinese company raw-data JSON snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and financial analysts use this skill to convert populated CN raw-data snapshots into an 8-section banker memo for credit review and equity investment workflows. It is intended to produce a Markdown memo and a hard-number provenance table before handoff to a separate slide-generation step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted raw-data snapshots, filenames, or path values could influence the generated memo or where outputs are written.

Mitigation: Use the skill only in a scoped project workspace with trusted raw-data JSON snapshots and a dedicated output directory.

Risk: The generated financial memo can contain incorrect or misleading analysis if source data is incomplete, inconsistent, or adversarial.

Mitigation: Review the generated memo and provenance table before using them for credit, investment, or client-facing decisions.

## Reference(s):

- [Banker Memo MD Canonical Prompt Template](artifact/references/banker_memo_md_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and plain-text prompt output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis.md and data-provenance.md only to the selected output directory.]

## Skill Version(s):

0.9.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
