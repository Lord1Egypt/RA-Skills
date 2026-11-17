## Description:

Fetches curated Agent Vitamins briefs with actionable improvements that an AI agent can assess, recommend, and execute after owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[menkesu](https://clawhub.ai/user/menkesu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep AI agents current with daily ecosystem briefs, select relevant improvements, and apply approved changes intentionally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an MCP package launched through npx, which can introduce package supply-chain and unattended execution risk.

Mitigation: Pin and verify the MCP package version before installation, and avoid unattended npx execution where possible.

Risk: The full daily brief requires an Agent Vitamins token.

Mitigation: Store the token only in an approved secret manager and avoid exposing it in prompts, logs, or shared configuration.

Risk: Daily brief recommendations may cause changes to an agent's behavior, tools, memory, or configuration.

Mitigation: Use the skill's approval workflow: review recommendations, select only relevant changes, and implement them only after explicit owner approval.

Risk: Generic session-start or self-improvement prompts could trigger the skill more broadly than intended.

Mitigation: Invoke the skill explicitly for Agent Vitamins review workflows and keep automatic use disabled unless reviewed by the owner.

## Reference(s):

- [Agent Vitamins](https://agentvitamins.com)
- [ClawHub skill release](https://clawhub.ai/menkesu/skills/agent-vitamins)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with recommendations, configuration snippets, and implementation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preview mode returns brief titles and categories; full actionable briefs require an Agent Vitamins subscription token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
