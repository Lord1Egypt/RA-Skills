## Description:

Load this skill when users ask about Web3 DAO governance. Use the Degov Agent API as the primary source for DAO governance facts and recent activity, then use web search as a secondary layer when API coverage is missing, stale, or insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boundless-forest](https://clawhub.ai/user/boundless-forest)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer Web3 DAO governance questions with current Degov Agent API data and source follow-up when API coverage is missing or needs verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Degov Agent API calls can authorize x402 wallet payments without strong local spending limits or endpoint controls.

Mitigation: Require explicit user consent before paid endpoints, keep only a small USDC balance in the dedicated Base wallet, check budget guidance before use, and avoid alternate API endpoints except trusted development systems.

Risk: The local wallet and passphrase files are sensitive secrets.

Mitigation: Use the generated wallet only for API payments, rely on encrypted wallet storage with restricted file permissions, and do not share wallet or passphrase files.

Risk: DAO governance answers can become misleading if API coverage is stale, missing, or too shallow.

Mitigation: Check data freshness when relevant and use official DAO forums, proposal pages, governance portals, or web follow-up before presenting important claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boundless-forest/skills/degov-agent-skills)
- [Degov Agent API](https://agent-api.degov.ai)
- [Base mainnet RPC endpoint](https://mainnet.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise prose, source links, and inline shell commands when wallet or API setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Degov Agent API data, web follow-up, wallet funding guidance, and payment settlement links; raw API payloads are avoided unless requested.]

## Skill Version(s):

0.6.1 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
