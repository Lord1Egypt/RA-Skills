## Description:

Checks a DeepSeek API account balance and reports total, granted, topped-up, and account availability details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liflife](https://clawhub.ai/user/liflife)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API users use this skill to check DeepSeek account balance from a terminal when they need current quota, remaining balance, or account availability information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If DEEPSEEK_API_KEY is unset, the skill can fall back to ANTHROPIC_AUTH_TOKEN and send that token to DeepSeek.

Mitigation: Use only a dedicated DEEPSEEK_API_KEY, avoid the ANTHROPIC_AUTH_TOKEN fallback, and rotate any Anthropic token previously exposed through this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liflife/skills/deepseek-balance)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with bash code blocks and terminal output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DeepSeek API key environment variable for normal use.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
