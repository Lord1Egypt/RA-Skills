## Description:

Run a weekly token-optimization audit for durable instruction files in any OpenClaw workspace, generate a markdown report, and propose approval-gated cleanup actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyylin](https://clawhub.ai/user/andyylin)

### License/Terms of Use:


## Use Case:

Developers and workspace maintainers use this skill to audit durable instruction files for token-heavy content, stale markers, and cleanup candidates while preserving an explicit approval step before removals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the audit against the wrong workspace could include unintended durable instruction files in the generated report.

Mitigation: Run the skill only against a workspace you intend to review and inspect the generated report before sharing or acting on it.

Risk: Cleanup proposals could remove useful instructions if accepted without review.

Mitigation: Require explicit user approval before deletion or compaction and apply only approved cleanup batches.

## Reference(s):

- [Publish Safety Notes](references/publish-safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report plus concise chat guidance and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated report under knowledge/reports/durable-files by default; cleanup edits require explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata and RELEASE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
