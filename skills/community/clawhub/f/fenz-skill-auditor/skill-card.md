## Description:

Audits Claude skills from GitHub repositories for effectiveness, token usage, safety, and best-practice compliance, then automatically generates bilingual social media posts about the findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangran](https://clawhub.ai/user/yangran)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit Claude skill repositories, generate structured audit reports, and create bilingual social media summaries of the findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow clones public GitHub repositories and copies skill source into local audit artifacts.

Mitigation: Run it only on repositories you intend to inspect, keep audit output in a scoped workspace, and avoid untrusted repositories with symlinks until file containment and size limits are fixed.

Risk: The workflow automatically generates branded bilingual social post drafts from audit findings.

Mitigation: Treat social-post generation as opt-in editorial output and review all drafts before publishing or sharing them.

Risk: The social-post step depends on an external sibling post-generator path outside the skill package.

Mitigation: Use that step only when the sibling dependency is present from a trusted source and has been reviewed.

## Reference(s):

- [Skill Audit Criteria](references/audit-criteria.md)
- [Skill Best Practices Checklist](references/skill-best-practices.md)
- [Skill Audit Report Template](assets/audit-report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/yangran/skills/fenz-skill-auditor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON metadata, process logs, and bilingual Markdown post drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an audit output directory containing source copies, metadata, an audit report, a process log, and optional English and Chinese post drafts.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
