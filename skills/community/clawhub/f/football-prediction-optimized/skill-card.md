## Description:

Helps agents screen batches of football matches and produce single-match win/draw/loss predictions with confidence, CLV estimates, reasoning, and risk factors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingvergil](https://clawhub.ai/user/kingvergil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to compare football matches for prediction quality, select promising fixtures, and generate structured match predictions. It is intended for advisory analysis and should not be treated as validated financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Match feature text and related user-provided data may be sent to DeepSeek or another configured compatible endpoint.

Mitigation: Use the skill only with data appropriate for that endpoint, and avoid proprietary betting, account, or sensitive personal data in inputs.

Risk: A configurable API base URL can receive the DeepSeek API credential if set to an untrusted endpoint.

Mitigation: Leave DEEPSEEK_BASE_URL unset or set it only to a trusted HTTPS endpoint intended to receive the credential.

Risk: Football predictions and CLV estimates can be incorrect or misleading if treated as financial advice.

Mitigation: Treat outputs as advisory analysis, independently review assumptions and risk factors, and avoid automated betting decisions based solely on the skill output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingvergil/skills/football-prediction-optimized)

## Skill Output:

**Output Type(s):** [JSON, Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [JSON objects for batch screening or single-match prediction, with optional Markdown and shell-command guidance from the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires football match feature text as input and a DeepSeek-compatible API key when running the bundled Python script.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
