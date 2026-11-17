## Description:

Access the Alternative.me Crypto Fear & Greed Index to anchor baseline market sentiment analysis around Extreme Fear or Extreme Greed conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arielcaba-dev](https://clawhub.ai/user/arielcaba-dev)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch the Alternative.me Crypto Fear & Greed Index and incorporate the current sentiment score and classification into crypto market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make a network request to Alternative.me to retrieve public market sentiment data.

Mitigation: Review outbound network access policies before use and allow the Alternative.me endpoint only when the request is appropriate for the environment.

Risk: The Fear & Greed score is a market sentiment signal and can be misleading if treated as investment advice or a complete risk assessment.

Mitigation: Use the score as one input alongside other market, technical, and risk analysis before making decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arielcaba-dev/skills/fear-and-greed-index)
- [Publisher Profile](https://clawhub.ai/user/arielcaba-dev)
- [Alternative.me Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [Alternative.me Fear & Greed API](https://api.alternative.me/fng/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and JSON field descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public sentiment data fields including value, value_classification, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
