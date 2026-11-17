## Description:

AI Investment Analyzer helps agents draft investment analysis, portfolio optimization, risk assessment, and market forecast reports for assets such as stocks, cryptocurrency, real estate, forex, commodities, bonds, and funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwz747512353](https://clawhub.ai/user/mwz747512353)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft investment analysis, risk review, portfolio allocation, and market forecast text. It should be treated as decision-support content, not as verified financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A ClawHub token is exposed in the distributed artifact.

Mitigation: Revoke the token, remove it from all released copies, and audit for any use before installing or redistributing the skill.

Risk: Mock financial outputs are presented as investment guidance.

Mitigation: Do not use the output for real investment decisions unless verified market data, clear timestamps, validated methods, and prominent financial-risk disclaimers are added.

Risk: Analysis requests and results may be saved locally in analysis_log.json.

Mitigation: Disclose local logging to users, review retention needs, and remove or anonymize saved analysis records when appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mwz747512353/skills/ai-investment-analyzer)
- [Project homepage from ClawHub metadata](https://github.com/AIFinanceAssistant/ai-investment-analyzer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text reports with command examples and JSON-compatible analysis records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Analysis commands may append local records to analysis_log.json.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact files list 1.0.0 and 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
