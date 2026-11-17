## Description:

Generates review-first desktop cleanup plans, classification rules, and phased organization schedules from a desktop folder or file list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to audit a desktop folder or file list and produce a reviewable cleanup plan before moving or deleting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated cleanup plan could lead to accidental file moves or deletions if followed without review.

Mitigation: Review the plan and confirmation checklist before taking action, and use dry-run or read-only audit workflows where possible.

Risk: Broad input paths can expose unrelated personal or sensitive files during desktop analysis.

Mitigation: Point the skill at a specific desktop folder or curated file list, and remove sensitive material from inputs when practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/desktop-cleanup-playbook)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown by default, with optional JSON output from the local support script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable plans, risk notes, confirmation checklists, and optional dry-run directory audit reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
