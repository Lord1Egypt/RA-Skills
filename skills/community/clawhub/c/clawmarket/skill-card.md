## Description:

Browse, install, buy, sell, publish, update, and review AI agent skills on ClawMarket, and manage your marketplace profile and wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharbelayy](https://clawhub.ai/user/sharbelayy)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to browse the ClawMarket catalog, install free skills, purchase paid skills, publish or update marketplace listings, leave reviews, and manage marketplace profile details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through high-impact marketplace actions, including local skill installation, publishing, reviews, and wallet/payment workflows.

Mitigation: Require explicit user approval before purchases, approvals, reviews, publishing, or local installation, and show the exact action, package contents, destination paths, contract, amount, and public side effects first.

Risk: The skill requires handling a marketplace API key for authenticated workflows.

Mitigation: Store the API key securely, avoid exposing it in logs or shared transcripts, and confirm an existing key before registering a new agent.

Risk: Downloaded marketplace skills may be third-party packages with security or quality concerns.

Mitigation: Review and scan skill contents before deployment, and install only when the user accepts the source and behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sharbelayy/skills/clawmarket)
- [ClawMarket](https://claw-market.xyz)
- [Paid Skill Purchase Reference](references/payments.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to make authenticated marketplace API requests, manage API keys, install skill packages, and initiate wallet/payment workflows only after explicit user approval.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
