## Description:

Agent Orchestrator manages durable coding agents such as Claude Code, Codex, and OpenCode so users can spawn agents, track progress, route PR review and CI feedback, and manage sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[illegalcall](https://clawhub.ai/user/illegalcall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate coding work, issue handling, PR follow-up, CI remediation, and session management to durable coding agents through AO.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route coding, issue, status, and follow-up requests into persistent agent workflows that may affect repositories and pull requests.

Mitigation: Require explicit user confirmation before spawning or batch-spawning agents, present the intended work plainly, and verify results before relying on generated changes.

Risk: AO workflows may use GitHub CLI credentials, Anthropic API credentials, worktrees, PR activity, and persistent sessions.

Mitigation: Use dedicated least-privilege GitHub and LLM credentials, set spending limits where available, and avoid placing .env files or other secrets in agent worktrees.

Risk: Broad plugin access can expose more tools than are needed for a given deployment.

Mitigation: Review installed plugins and enable only the AO and OpenClaw tool access needed for the intended repositories and workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/illegalcall/skills/composio-agent-orchestrator)
- [Agent Orchestrator Config Reference](artifact/references/config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command, configuration, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup commands, AO configuration examples, and operational guidance for agent orchestration workflows.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
