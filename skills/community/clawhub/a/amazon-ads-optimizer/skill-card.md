## Description:

Amazon Ads Optimizer helps Amazon sellers evaluate advertising performance, set bid guardrails, analyze flywheel opportunities, generate negative keyword recommendations, and draft short video ad scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers use this skill to review user-provided campaign metrics, identify profit-protection actions, plan bid and budget changes, and generate ad strategy guidance without connecting to external ad accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid, budget, keyword, or pause recommendations could affect advertising spend if applied manually without review.

Mitigation: Review each recommendation against current Amazon Ads data, margin targets, and business constraints before making account changes.

Risk: Analysis quality depends on the completeness and accuracy of user-provided advertising metrics.

Mitigation: Provide recent campaign, keyword, ACoS, budget, conversion, and organic ranking data, and treat missing-data recommendations as directional.

Risk: The skill is primarily written for Chinese-language Amazon Ads advisory workflows.

Mitigation: Use an operator fluent in the output language or translate and review the recommendations before execution.

## Reference(s):

- [Flywheel bid strategy reference](references/bid-strategies.md)
- [ClawHub skill page](https://clawhub.ai/wangm-a3/skills/amazon-ads-optimizer)
- [Project homepage](https://xiaping.coze.site)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports, plain-text recommendations, optional JSON from the calculator script, and shell commands for local calculations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; users provide advertising metrics manually and review recommendations before applying them in Amazon Ads.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
