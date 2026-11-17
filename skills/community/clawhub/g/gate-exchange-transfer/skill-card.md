## Description:

Gate Exchange same-UID internal transfer skill. Use when the user asks to move funds between their own Gate accounts. Triggers on 'transfer funds', 'move USDT to futures', 'internal transfer'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare, confirm, execute, and verify same-UID transfers between their own Gate spot, isolated margin, perpetual, delivery, and options accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Gate MCP session can perform same-UID internal transfers with funds.

Mitigation: Install only when this behavior is intended, keep the API key limited to the documented permissions, and require an explicit transfer draft confirmation before execution.

Risk: Internal transfers may be irreversible if the user confirms an incorrect account, asset, or amount.

Mitigation: Carefully verify the source account, destination account, currency, amount, and any conditional parameters in the transfer draft before confirming.

Risk: Secrets could be exposed if credentials are pasted into chat instead of configured locally.

Mitigation: Use the local Gate MCP session with GATE_API_KEY and GATE_API_SECRET and never paste API secrets into chat.

## Reference(s):

- [Gate Skills Homepage](https://github.com/gate/gate-skills)
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage)
- [Gate Internal Transfer Runtime Rules](references/gate-runtime-rules.md)
- [Gate Exchange Transfer MCP Specification](references/mcp.md)

## Skill Output:

**Output Type(s):** [Markdown, API calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown transfer drafts, confirmation prompts, execution results, verification summaries, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Gate MCP session with GATE_API_KEY and GATE_API_SECRET; write actions require explicit immediate user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter version 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
