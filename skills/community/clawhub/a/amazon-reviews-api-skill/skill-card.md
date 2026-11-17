## Description:

This skill helps an agent extract structured Amazon product reviews by ASIN through BrowserAct's Amazon Reviews API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Amazon review text, ratings, reviewer metadata, verified-purchase status, and publication details for product feedback analysis, competitor research, sentiment monitoring, and quality insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a BrowserAct API key and its source asks users to provide one through the agent conversation.

Mitigation: Configure BROWSERACT_API_KEY directly in the environment or a secret manager, and do not paste API keys into chat.

Risk: Extracted review data can include reviewer names and profile links.

Mitigation: Use, store, and share extracted reviewer data only where there is a legitimate basis and appropriate privacy handling.

Risk: The security verdict is suspicious because live review extraction and data collection may create policy, privacy, or terms-of-use concerns.

Mitigation: Use the skill only when live Amazon review extraction is explicitly needed, and review applicable data-use requirements before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/phheng/skills/amazon-reviews-api-skill)
- [BrowserAct API key setup](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API base URL](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with structured review fields and possible JSON fallback output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSERACT_API_KEY and an Amazon ASIN; polls BrowserAct task status until completion.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
