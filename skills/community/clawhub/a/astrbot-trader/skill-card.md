## Description:

Astrbot Trader defines an AstrBot cryptocurrency trading persona for monitoring holdings, generating trading recommendations, and drafting market content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators use this skill to configure an AstrBot trading agent that monitors OKX positions and prices, checks simple EMA/BOLL signals, drafts Substack and Twitter content, and prepares customer outreach text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains exchange credentials and portfolio data.

Mitigation: Treat any matching credentials as compromised, rotate them, and remove secrets and account data before use.

Risk: The skill asks for broad recurring authority over trading, order changes, publishing, direct messages, and synchronization.

Mitigation: Require explicit user confirmation before trades, order changes, publishing, direct messages, or synchronization.

Risk: The artifact references disabled TLS verification for OKX API access.

Mitigation: Keep TLS verification enabled and use read-only credentials for monitoring workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/skills/astrbot-trader)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Concise text or Markdown with trading status, recommendations, content drafts, outreach copy, and operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial, trading, publishing, messaging, and synchronization actions should require explicit user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
