## Description:

Audits OpenClaw Gateway cron jobs from jobs.json or CLI output, classifies scheduled workloads by token cost, and suggests when OS timers plus scripts and openclaw message send could replace recurring LLM runs without editing jobs automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x3r081](https://clawhub.ai/user/x3r081)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review OpenClaw Gateway cron schedules, identify recurring agent-turn workloads that may spend tokens on every run, and receive cautious manual migration guidance for jobs that can be handled by OS timers and scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional `npx clawhub@latest install` command can resolve to a different CLI version over time.

Mitigation: Pin or verify the ClawHub CLI version when reproducibility matters.

Risk: Cron job prompts and payloads may contain private operational details.

Mitigation: Review prompts carefully and follow the skill's instruction to redact secrets, API keys, chat IDs, and other sensitive values in summaries.

Risk: Manual migration guidance could cause duplicate scheduled messages if the original Gateway cron remains enabled.

Mitigation: After a human-led migration, disable or remove the old Gateway cron entry and verify the new timer fires once at the intended time.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/x3r081/skills/cron-job-token-auditor)
- [Publisher profile](https://clawhub.ai/user/x3r081)
- [REFERENCE.md](REFERENCE.md)
- [README.md](README.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with tables, per-job summaries, numbered manual steps, and inline shell or configuration examples when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only guidance; the skill instructs the agent to redact sensitive values, avoid guaranteed savings claims, and avoid automatic cron or system configuration changes.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
