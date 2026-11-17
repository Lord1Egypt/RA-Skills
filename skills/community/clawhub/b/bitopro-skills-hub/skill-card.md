## Description:

BitoPro Spot lets an agent query BitoPro public spot market data and, when credentials are configured, perform authenticated account, order, deposit, withdrawal, and TWD trading workflows with explicit trading safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitopro](https://clawhub.ai/user/bitopro)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent retrieve BitoPro spot market data and operate authenticated spot trading and account workflows on their behalf. It is suited for public market checks, account review, order management, and withdrawal workflows where the user controls exchange credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured private credentials can let an agent access account data and perform real trading or withdrawal actions on BitoPro.

Mitigation: Use read-only API keys unless trading is required, scope exchange/API permissions narrowly, and only install the skill when agent access to BitoPro is intended.

Risk: Order placement, batch orders, cancellations, and withdrawals can have financial consequences if the user approves the wrong action.

Mitigation: Require explicit review of displayed order or withdrawal details before execution, including amount, pair, side, price, fee, destination, and network where applicable.

Risk: Approved strategy sessions can place bounded follow-up orders without asking for confirmation at every step.

Mitigation: Set conservative session limits for single-order size, total exposure, daily loss, maximum steps, and expiry, and configure BITOPRO_SPOT_SINGLE_ORDER_MAX_QUOTE for activity outside approved sessions.

Risk: API secrets or sensitive account details could be exposed if echoed in agent output.

Mitigation: Keep credentials in environment variables, mask API keys in user-facing text, and never display BITOPRO_API_SECRET.

## Reference(s):

- [BitoPro API Authentication](references/authentication.md)
- [BitoPro API Endpoints Reference](references/endpoints.md)
- [ClawHub skill page](https://clawhub.ai/bitopro/skills/bitopro-skills-hub)
- [BitoPro publisher profile](https://clawhub.ai/user/bitopro)
- [BitoPro withdrawal address management](https://www.bitopro.com/address)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown or structured JSON-like API results with concise trading, account, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require BITOPRO_API_KEY, BITOPRO_API_SECRET, and BITOPRO_EMAIL for private account, trading, and withdrawal actions; public market-data actions do not require credentials.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 2.5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
