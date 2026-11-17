## Description:

Uses the ClawEC API to analyze Amazon keywords through ABA research, keyword mining, keyword trends, and optional AI interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, ecommerce operators, and their agent workflows use this skill to submit keyword searches to ClawEC and retrieve ABA data, keyword mining results, trend data, and optional AI analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits Amazon keyword, region, month, and selected analysis options to ClawEC.

Mitigation: Use the skill only when ClawEC is an approved service for that data.

Risk: The skill requires a ClawEC API key.

Mitigation: Store CLAWEC_API_KEY as a secret environment variable and avoid hardcoding it in files or prompts.

Risk: Concurrent identical searches in shared ClawEC accounts may cause search_and_poll.sh to retrieve the wrong matching history record.

Mitigation: Avoid shared accounts or concurrent identical searches when using the polling workflow; verify the returned log ID and parameters before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-amazon-keyword-search)
- [ClawEC API base](https://www.clawec.com/api)
- [ClawEC API key setup](https://www.clawec.com/api-key?source=q-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON API responses, Markdown AI analysis, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEC_API_KEY; optional AI interpretation may require polling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
