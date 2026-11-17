## Description:

Multi-agent architecture where an AI agent operates as the CEO of growth operations, reads strategic intent, delegates to specialized sub-agents, and delivers production output coordinated through GitHub Issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams operating AI-assisted growth or DevOps workflows use this skill as a deployable multi-agent workspace: a CEO agent interprets strategic direction, delegates GitHub Issue tasks to Growth and DevOps leaders, and routes production changes through human PR review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous server execution, scheduled cron tasks, and GitHub-write workflows can make broad changes if installed without review.

Mitigation: Run only as a dedicated non-root user in a test or tightly scoped repository, and keep cron disabled until every scheduled skill and approval boundary has been reviewed.

Risk: The skill expects LLM API keys and GitHub credentials, which can expand impact if over-privileged or stored carelessly.

Mitigation: Use least-privilege GitHub tokens, avoid plaintext .env secrets where possible, and restrict credentials to the minimum repository and task scope.

Risk: Runtime installation and agent execution depend on external tooling that may change over time.

Mitigation: Pin and verify the OpenClaw runtime or chosen autonomous-agent framework before deployment.

## Reference(s):

- [Hermes Agent CEO Architecture](https://emergence.science/en/articles/hermes-agent-ceo-architecture)
- [ClawHub skill page](https://clawhub.ai/emergencescience/skills/emergence-agent-ceo)
- [Quickstart](docs/quickstart.md)
- [Two-tier setup](docs/two-tier-setup.md)
- [Heartbeat schedule](HEARTBEAT.md)
- [DevOps leader runbook](ops/DEVOPS_LEADER_RUNBOOK.md)
- [Growth leader runbook](ops/GROWTH_LEADER_RUNBOOK.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands, issue templates, runbooks, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a deployable workspace scaffold and operational guidance; external publishing, deployment, spending, and PR merges remain human-approved.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
