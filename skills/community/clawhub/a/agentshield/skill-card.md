## Description:

AI Agent Detection and Response for real-time security monitoring with Sigma rules and optional LLM-powered triage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markbriers](https://clawhub.ai/user/markbriers)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and security engineers use AgentShield to monitor AI agent tool calls, evaluate activity against Sigma-style rules, and triage suspicious events before allowing or blocking actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer pulls remote AgentShield releases, Go module code, rules, and an OpenClaw plugin during installation.

Mitigation: Install only after trusting the AgentShield release process and npm plugin publisher; prefer pinned versions or verified artifacts before sensitive use.

Risk: The installed service runs persistently and can observe or block AI agent tool-call and lifecycle events.

Mitigation: Review the OpenClaw plugin configuration and run in audit or shadow mode first when validating behavior in a new environment.

Risk: Optional LLM triage may send suspicious-event context to a configured model provider.

Mitigation: Enable triage only with an approved provider and avoid sending sensitive work context unless the deployment's data-handling requirements are satisfied.

## Reference(s):

- [ClawHub AgentShield Skill](https://clawhub.ai/markbriers/skills/agentshield)
- [AgentShield GitHub Repository](https://github.com/agentshield-ai/agentshield)
- [AgentShield Sigma Rules Repository](https://github.com/agentshield-ai/sigma-ai.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline bash, YAML, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets Linux and macOS on amd64 and arm64; requires either Go or curl for installation.]

## Skill Version(s):

2.0.2 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
