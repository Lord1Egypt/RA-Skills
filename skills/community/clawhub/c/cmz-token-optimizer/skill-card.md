## Description:

Routes OpenClaw prompts that require tools to paid Bailian models and plain chat to free OpenRouter models, while offering context, heartbeat, and token-budget optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmz666666](https://clawhub.ai/user/cmz666666)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to reduce context-loading and API costs by classifying prompts, recommending model routes, generating optimized agent guidance, tuning heartbeat cadence, and checking token budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent or heartbeat guidance may change context loading, routing, or scheduling behavior in ways that affect task quality or cost.

Mitigation: Review AGENTS.md.optimized and HEARTBEAT.md changes manually before replacing existing workspace files.

Risk: Optional provider-routing examples and companion-skill or GitHub clone instructions can introduce provider, credential, privacy, cost, or dependency changes if followed without review.

Mitigation: Confirm provider choices, model policies, credentials, privacy requirements, and install sources before applying optional configuration.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cmz666666/skills/cmz-token-optimizer)
- [Publisher profile](https://clawhub.ai/user/cmz666666)
- [Clawdis homepage](https://github.com/Asif2BD/OpenClaw-Token-Optimizer)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON CLI results, shell commands, and generated local configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local OpenClaw workspace state files and generated guidance such as AGENTS.md.optimized or HEARTBEAT.md when users run the scripts.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
