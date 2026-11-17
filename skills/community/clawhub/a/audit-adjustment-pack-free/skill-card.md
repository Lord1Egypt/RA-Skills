## Description:

A local checker for audit adjustment worksheets that runs 14 built-in checks per audited entity directory and prints one conclusion line per entity with source file and line references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Audit assistants, audit managers, and finance review staff use this skill to check exported audit adjustment workpapers across trial balance, adjustment entries, impairment, depreciation, amortization, provisions, cash count, and settlement checks. It helps produce per-entity conclusions with source citations for review, but it does not replace professional audit judgment or issue assurance opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit and accounting workpapers may contain sensitive entity names, file names, line numbers, and findings that are printed to the terminal or agent transcript.

Mitigation: Run the skill only on intended exported workpaper directories and handle terminal output and transcripts as sensitive audit material.

Risk: The skill checks disclosed worksheet relationships and can report material as unexecuted or insufficient when required inputs are missing.

Mitigation: Review source-cited findings and the list of unexecuted checks before relying on the output in an audit or finance review workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/audit-adjustment-pack-free)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Terminal text by default, with optional JSON output when run with --json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs per-entity conclusions, finding details, source file and line references, status fields, and disclosed unexecuted checks; it writes results to stdout rather than creating files.]

## Skill Version(s):

1.0.28 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
