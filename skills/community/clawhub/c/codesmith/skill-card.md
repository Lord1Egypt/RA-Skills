## Description:

CodeSmith is a senior engineering agent configuration for OpenClaw agents that do full-stack development automation, CI/CD, GitHub workflows, ACP dispatch, and production coding work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawmentorai](https://clawhub.ai/user/clawmentorai)

### License/Terms of Use:


## Use Case:

Developers and engineers use CodeSmith to configure OpenClaw agents for repository maintenance, CI/CD workflows, GitHub operations, sub-agent dispatch, scheduled briefs, and supervised overnight branch-based work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ready-enabled scheduled autonomous jobs can perform briefs, health checks, and overnight work without active supervision.

Mitigation: Review cron-patterns.json before installation, set cron templates to disabled first, enable one job at a time, and require human approval for overnight work.

Risk: GitHub and deployment API guidance can affect repositories or hosting environments when used with broad credentials.

Mitigation: Use narrowly scoped GitHub and hosting tokens, limit jobs to approved repositories and branches, and require human approval for every deployment API call.

## Reference(s):

- [CodeSmith ClawHub Skill Page](https://clawhub.ai/clawmentorai/skills/codesmith)
- [CodeSmith Mentor Package](artifact/CLAW_MENTOR.md)
- [CodeSmith Skill Definition](artifact/SKILL.md)
- [Setup Guide](artifact/setup-guide.md)
- [Privacy Notes](artifact/privacy-notes.md)
- [Cron Patterns](artifact/cron-patterns.json)
- [Working Patterns](artifact/working-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON cron templates, shell command snippets, and configuration text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scheduled job templates and deployment guidance that should be reviewed before enabling.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md, CLAW_MENTOR.md, cron-patterns.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
