## Description:

Interact with a Public.com brokerage account through the Public.com API to view accounts, portfolios, orders, history, instruments, quotes, options data, and to preflight, place, or cancel trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarricsookdeo](https://clawhub.ai/user/tarricsookdeo)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to connect an agent to a Public.com brokerage account for account review, market data lookup, order management, and options strategy guidance. It can support live trading workflows, so users should treat every order, cancellation, and strategy action as requiring explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use live brokerage authority to place or cancel trades.

Mitigation: Require explicit human approval for every live order, cancellation, and options strategy action.

Risk: The skill requires brokerage credentials and account identifiers.

Mitigation: Configure credentials outside chat when possible and use least-privilege API permissions.

Risk: The skill may install runtime dependencies before making API calls.

Mitigation: Preinstall dependencies in a controlled environment before use.

Risk: Options automation can expose users to complex financial losses.

Mitigation: Use preflight checks and review strategy assumptions, breakpoints, and account impact before any executable trade.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tarricsookdeo/skills/claw-skill-public-dot-com)
- [Public.com API settings](https://public.com/settings/v2/api)
- [Public.com signup](https://public.com/signup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code examples, and summarized script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Public.com API actions using configured brokerage credentials; live order, cancellation, and options strategy actions should require explicit human approval.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
