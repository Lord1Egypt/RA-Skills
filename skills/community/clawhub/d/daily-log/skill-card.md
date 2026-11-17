## Description:

Daily Log helps an agent write structured Markdown daily work logs at memory/daily/YYYY-MM/YYYY-MM-DD.md after sessions or important tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preserve detailed records of an agent's own work, decisions, changed files, commands, outputs, and errors for later memory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent daily logs may retain tokens, credentials, private configuration, customer data, or other sensitive command output.

Mitigation: Avoid using the skill after sensitive output unless a redaction, review, and deletion policy is in place.

Risk: Path convention drift can create duplicate daily logs for the same date.

Mitigation: Use the v1.3.0 path convention memory/daily/YYYY-MM/YYYY-MM-DD.md and check for an existing file before writing.

## Reference(s):

- [Daily Log Detailed Specification](references/spec.md)
- [ClawHub Skill Page](https://clawhub.ai/axelhu/skills/daily-log)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [Markdown daily log file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates persistent logs under memory/daily/YYYY-MM/YYYY-MM-DD.md while preserving existing entries.]

## Skill Version(s):

1.3.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
