## Description:

Pre-generates scheduled tenant content during an off-peak window, runs generation and quality checks through the content orchestrator, caches ready content for fast publishing, and reports generation, retry, timeout, degradation, and fairness metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to batch pre-generate daily content for active tenants, retry failed pre-generation jobs, and review JSON execution summaries before later publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly mark tenant and system publishing queues as content-ready.

Mitigation: Require explicit tenant and date scoping, plus dry-run or confirmation before any all-tenant execution.

Risk: Publishing-readiness changes may be hard to review after execution.

Mitigation: Use audit logging and review affected task_queue and content_pre_cache records before production scheduling.

Risk: Administrative execution may permit wider tenant impact than intended.

Mitigation: Run only in environments where broad tenant changes are acceptable, or narrow/remove the system-wide content_publish updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-pregenerator)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [JSON execution summary with supporting Markdown usage examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, DATABASE_URL, and configured agency-portal-mcp and postgres-mcp services.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
