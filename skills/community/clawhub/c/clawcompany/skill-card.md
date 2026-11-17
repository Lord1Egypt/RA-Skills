## Description:

ClawCompany coordinates PM, development, and review agents to turn feature or app requests into implementation tasks, code changes, and review results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-miao](https://clawhub.ai/user/felix-miao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to delegate a software request to a small virtual team that analyzes requirements, generates or modifies project code, and reviews the result. It is intended for rapid prototyping and implementation workflows in OpenClaw-style agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch coding agents that modify project files using broad natural-language triggers.

Mitigation: Install and run it in a disposable or version-controlled project directory, use dry-run first, and review generated changes before applying or committing them.

Risk: Task prompts and project details may be sent to external agent or model services.

Mitigation: Avoid sensitive prompts and proprietary project context unless the publisher documents acceptable data handling for the configured services.

Risk: Verbose operation or generated logs may expose credentials or sensitive configuration such as GLM_API_KEY.

Mitigation: Keep API keys in environment variables, avoid verbose mode with real secrets, and rotate any credential that appears in logs or generated output.

## Reference(s):

- [ClawCompany ClawHub release](https://clawhub.ai/felix-miao/skills/clawcompany)
- [OpenClaw](https://openclaw.ai)
- [GLM API key portal](https://open.bigmodel.cn/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON-style task plans, generated file paths or code changes, review summaries, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run and verbose modes; generated files and summaries depend on the downstream agent sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
