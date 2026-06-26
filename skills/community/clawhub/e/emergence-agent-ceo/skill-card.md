## Description: <br>
Multi-agent architecture where an AI agent operates as the CEO of growth operations, reads strategic intent, delegates to specialized sub-agents, and delivers production output coordinated through GitHub Issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emergencescience](https://clawhub.ai/user/emergencescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scaffold and run a GitHub-coordinated autonomous agent team for growth operations, content drafting, market research, DevOps monitoring, and PR-based human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous autonomous operation with GitHub credentials can modify repository state unexpectedly. <br>
Mitigation: Run first in a controlled test or low-risk repository, use a dedicated bot or fine-grained token with minimum repository access, protect branches, and require PR review. <br>
Risk: The skill uses sensitive LLM and GitHub credentials through environment configuration. <br>
Mitigation: Keep .env out of version control, restrict file permissions, rotate credentials when needed, and avoid broad organization tokens. <br>
Risk: The DevOps workflow may identify production, deployment, billing, or organization-level actions. <br>
Mitigation: Add explicit approval gates for production deployment, billing, and broad organization credentials; keep direct deployment actions with a human operator. <br>
Risk: Generated content, market analysis, and operational guidance may be incorrect or stale. <br>
Mitigation: Require human review for public publishing, PR merges, strategic decisions, and factual claims before external release. <br>
Risk: Cron-based execution can hide repeated failures or unexpected behavior if left unmonitored. <br>
Mitigation: Monitor cron output, issue comments, pull requests, and incident logs; pause the agent when anomalies appear. <br>


## Reference(s): <br>
- [Emergence Hermes Agent CEO Architecture](https://emergence.science/en/articles/hermes-agent-ceo-architecture) <br>
- [ClawHub Skill Page](https://clawhub.ai/emergencescience/emergence-agent-ceo) <br>
- [Quickstart](docs/quickstart.md) <br>
- [Two-Tier Setup Guide](docs/two-tier-setup.md) <br>
- [DevOps Leader Runbook](ops/DEVOPS_LEADER_RUNBOOK.md) <br>
- [Growth Leader Runbook](ops/GROWTH_LEADER_RUNBOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, issue templates, runbooks, and scaffolded workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces GitHub issue comments, draft files, pull requests, runbook updates, and operational logs when connected to an agent runtime and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
