## Description:

Queries API account balances, subscription usage, and billing history across Volcengine, Alibaba Cloud, DeepSeek, MiniMax, and OpenRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and account operators use this skill to check API provider balances, recent bills, and remaining plan usage with configured billing credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-looking cloud keys are present in the bundled reference material.

Mitigation: Do not use the included credential examples, and rotate any matching or reused keys before using the skill.

Risk: The skill handles sensitive billing credentials and describes Base64 storage, which is reversible encoding rather than secret protection.

Mitigation: Use read-only billing credentials, store them outside source control with strict local permissions, and treat Base64 values as exposed if shared.

## Reference(s):

- [API billing interface reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/yifeiwang1981/skills/api-billing)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries external billing APIs and prints account balance, usage, or billing summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
