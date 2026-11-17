## Description:

Provides ClawEC API guidance and helper scripts for Amazon ABA product-selection research, including marketplace, date, category, search-mode, and optional AI interpretation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and Amazon sellers use this skill to run ClawEC Amazon ABA market-trend searches, inspect search history and details, and summarize keyword, brand, purchase-rate, and optional AI interpretation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search inputs and ClawEC account credentials to the ClawEC API.

Mitigation: Use a CLAWEC_API_KEY scoped to ClawEC, do not hardcode it, and avoid sending sensitive unrelated business data in search parameters.

Risk: Searches or AI interpretation may consume account points and create query history in the ClawEC account.

Mitigation: Confirm the intended marketplace, month, category, search mode, and aiInterpret setting before executing calls, and review account usage where cost or history matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-aba-selection)
- [ClawEC API base URL](https://www.clawec.com/api)
- [ClawEC account registration](https://www.clawec.com/?source=q-clawhub)
- [ClawEC API key page](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese summaries, tables, raw ClawEC response fields, and optional AI analysis text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
