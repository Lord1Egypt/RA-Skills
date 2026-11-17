## Description:

Alipay Authenticate Wallet helps an agent check, open, authorize, bind, or unbind Alipay AI payment wallet capability through the alipay-bot CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alipay](https://clawhub.ai/user/alipay)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to guide Alipay wallet authorization flows, including checking wallet status, opening payment capability, binding an authorization code, revoking authorization, and escalating unresolved issues to feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants the agent high-impact authority over wallet authorization, including binding, closing, or unbinding payment capability.

Mitigation: Use only when the publisher and package are trusted, and require explicit user confirmation before closing or unbinding payment capability.

Risk: Server security evidence reports unsafe command construction in the artifact.

Mitigation: Fix command handling to pass user values as safe arguments rather than shell strings before relying on the skill in sensitive payment-account workflows.

Risk: The skill installs and executes a persistent local npm CLI.

Mitigation: Review before installing and verify the fixed package version and integrity value before executing the CLI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alipay/skills/alipay-authenticate-wallet)
- [Alipay payment-skills homepage](https://github.com/alipay/payment-skills)
- [Alipay agent-payment npm package](https://www.npmjs.com/package/@alipay/agent-payment)
- [CLI setup](references/cli-setup.md)
- [Environment variables](references/env-vars.md)
- [Output rules](references/output-rules.md)
- [Image output rules](references/image-output.md)
- [Security and design notes](references/security.md)
- [Feedback process](references/feedback.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and user-facing CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment or authorization links and image paths returned by the CLI; CLI output is intended to be relayed without rewriting.]

## Skill Version(s):

1.0.11-beta.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
