## Description:

Compute who gets what at each exit price from a cap table, including liquidation preferences, conversion points, founder dilution, and a plain-English reading of payout thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, operators, investors, and advisors use this skill to model exit waterfalls from cap table inputs and compare stakeholder payouts across sale prices. It helps explain when preferences dominate, when conversion becomes rational, and where common shares begin to receive value.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require private cap table and financing details as inputs.

Mitigation: Use the minimum necessary data, avoid unnecessary external sharing, and follow the organization's handling requirements for confidential financing information.

Risk: The artifact references a helper script that was not included in the release artifact.

Mitigation: Only run such a script after verifying its source and contents separately.

Risk: The model is educational and uses stated simplifications such as pari passu preferences and uncapped participation.

Mitigation: Compare assumptions with the actual financing documents and verify material decisions with a licensed professional.

## Reference(s):

- [Exit Waterfall ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/exit-waterfall)
- [Exit Waterfall Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/exit-waterfall.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with payout tables, assumptions, plain-English interpretation, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented cap table input guidance and educational disclaimers; results should be checked against governing financing documents.]

## Skill Version(s):

50.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
