## Description:

Gate Exchange same-UID internal transfer skill for moving funds between a user's own Gate accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaixianggeng](https://clawhub.ai/user/gaixianggeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, confirm, and execute same-UID internal transfers between Gate spot, isolated margin, perpetual, delivery, and options accounts through a configured Gate MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires wallet write access and can move funds within the user's Gate account.

Mitigation: Use a Gate API key limited to the listed permissions, review every transfer draft, and confirm only when the amount, asset, source, and destination are correct.

Risk: Ambiguous, stale, or changed transfer parameters could cause an unintended transfer.

Mitigation: Execute only after an explicit confirmation in the immediately previous user turn, and require a new draft whenever amount, currency, source, or destination changes.

Risk: Missing MCP configuration, authentication failures, unsupported account routes, or insufficient balances can affect fund safety.

Mitigation: Stay in read-only guidance mode until configuration, permissions, account route, and source balance checks pass.

## Reference(s):

- [Gate Skills Homepage](https://github.com/gate/gate-skills)
- [Gate Internal Transfer Runtime Rules](references/gate-runtime-rules.md)
- [Gate Exchange Transfer MCP Specification](references/mcp.md)

## Skill Output:

**Output Type(s):** [markdown, API calls, guidance]

**Output Format:** [Markdown transfer drafts, confirmation prompts, transfer result reports, and setup or recovery guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit immediate confirmation before wallet write actions and verifies transfers through account-book read endpoints when available.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata; artifact frontmatter version: 2026.4.6-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
