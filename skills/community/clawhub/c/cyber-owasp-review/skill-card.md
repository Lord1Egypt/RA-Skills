## Description:

Map application security findings to OWASP Top 10 categories and generate remediation checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and application security reviewers use this skill to normalize scanner, test, or review findings into OWASP Top 10 categories and produce prioritized remediation checklist output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes local scanner findings and writes report artifacts to a user-provided output path.

Mitigation: Provide only intended scanner findings as input and choose a safe output path before execution.

Risk: Server security evidence identifies a limited dry-run file-write bug.

Mitigation: Do not rely on --dry-run to avoid filesystem changes until that behavior is fixed.

## Reference(s):

- [OWASP Mapping Guide](references/owasp-mapping-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/0x-professor/skills/cyber-owasp-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional JSON, CSV, or Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces category counts, normalized finding rows, remediation checklists, and local output artifacts.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
