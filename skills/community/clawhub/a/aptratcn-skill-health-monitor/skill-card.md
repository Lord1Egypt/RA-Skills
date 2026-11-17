## Description:

Automated audits that score and report on skill health by checking structure, content, activity, compatibility, and discoverability to prevent failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit skill collections, identify missing or stale documentation, score skill health, and produce action-oriented maintenance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad skill audits may cause an agent to inspect unrelated project files.

Mitigation: Point the agent at the specific skill directory or collection intended for review before running an audit.

Risk: Health scores can be misleading if repository state, dependencies, or framework compatibility are stale or incomplete.

Mitigation: Review reported findings against the current files and repository history before making maintenance decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aptratcn/skills/aptratcn-skill-health-monitor)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with checklist scores and suggested audit commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces skill health scores across structure, content, activity, compatibility, and discoverability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
