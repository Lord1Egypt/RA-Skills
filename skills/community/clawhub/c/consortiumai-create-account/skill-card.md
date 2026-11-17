## Description:

Create a custodial wallet account on Consortium AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webcraft3r](https://clawhub.ai/user/webcraft3r)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to create Consortium AI custodial wallet accounts for a supplied wallet address through the Consortium AI API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a wallet address and API key to Consortium AI to create a custodial wallet account.

Mitigation: Use it only when you trust Consortium AI for this workflow, prefer a dedicated scoped API key if available, and verify custody terms before using it with real funds or production users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/webcraft3r/skills/consortiumai-create-account)
- [Consortium AI](https://consortiumai.org/)
- [Consortium AI custodial wallet API endpoint](https://api.consortiumai.org/api/custodial-wallet/create-with-api-key)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRADING_ANALYSIS_API_KEY and a wallet address; the bundled script prints API responses as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
