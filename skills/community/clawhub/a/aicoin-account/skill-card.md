## Description:

Exchange account management for balances, positions, order history, registration, API key setup, tier checks, and related account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[procaross](https://clawhub.ai/user/procaross)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect exchange account data, manage AiCoin and exchange API key setup, retrieve referral registration links, check AiCoin data-tier access, and run supported exchange actions through Node.js scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill is framed as read-only but exposes broader financial actions and credential handling.

Mitigation: Use exchange API keys with the minimum permissions needed, preferably read-only unless trading, transfer, leverage, or margin actions are intentionally required.

Risk: Exchange account actions can include transfers and order creation when credential permissions allow them.

Mitigation: Review every proposed financial action before execution, confirm order or transfer details out of band when appropriate, and restrict API-key scopes at the exchange.

Risk: The security guidance warns against relying on automatic dependency installation.

Mitigation: Install and review dependencies explicitly before use instead of depending on runtime installation.

Risk: The security guidance says AICOIN_BASE_URL changes the API destination.

Mitigation: Leave AICOIN_BASE_URL unset unless the destination is trusted and intentionally selected.

Risk: Registration flows are steered through AiCoin referral links.

Mitigation: Disclose referral routing to users before directing registration or account-opening flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/procaross/skills/aicoin-account)
- [AiCoin Open Data](https://www.aicoin.com/opendata)
- [OpenClaw source metadata](https://github.com/aicoincom/coinos-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline Node.js shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local .env configuration and invoke exchange or AiCoin API scripts that return JSON.]

## Skill Version(s):

2.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
