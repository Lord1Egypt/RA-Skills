## Description:

Read-only health audit for recurring / scheduled AI agent jobs. Finds silent failures, duplicate active jobs, retry loops, over-frequent schedules, stale automations, risky model usage, and context bloat. Evidence first. Manual verification before any change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[choosenobody](https://clawhub.ai/user/choosenobody)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to audit recurring or scheduled AI agent jobs for silent failures, duplicate active schedules, retry loops, over-frequent runs, stale automations, risky model usage, and context bloat. It produces evidence and manual verification steps without changing jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit evidence may include operational details from scheduled agent jobs.

Mitigation: Redact secrets, IDs, private paths, payloads, and production details before sharing findings outside the owning team.

Risk: Global install commands and related skill suggestions could affect shared agent environments if run without review.

Mitigation: Review the target environment and any related skills separately before installing or upgrading global skills.

Risk: Findings about cron health can be mistaken for approval to edit, disable, delete, restart, or retune jobs.

Mitigation: Treat the output as read-only evidence and perform manual verification before changing schedules, prompts, models, or job state.

## Reference(s):

- [Agent Cron Audit on ClawHub](https://clawhub.ai/choosenobody/skills/agent-cron-audit)
- [choosenobody Publisher Profile](https://clawhub.ai/user/choosenobody)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline text and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-first findings with confidence labels, redacted observations, manual verification prompts, and read-only next steps.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
