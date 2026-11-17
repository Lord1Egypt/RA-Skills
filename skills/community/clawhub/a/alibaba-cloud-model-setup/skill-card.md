## Description:

Configures OpenClaw to use Alibaba Cloud Bailian as a model provider through an interactive flow covering plan type, site endpoint, API key handling, model selection, backups, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraterrest](https://clawhub.ai/user/extraterrest)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add, switch, or repair Alibaba Cloud/Qwen provider configuration in OpenClaw while preserving existing configuration where possible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit local OpenClaw configuration and change default models.

Mitigation: Review the target config path, keep the generated backup, and inspect the final JSON before restarting OpenClaw.

Risk: API keys can be exposed if passed on the command line or stored inline.

Mitigation: Use a scoped, rotatable Alibaba Cloud key and prefer environment-variable storage over command-line or inline storage.

Risk: The security evidence reports mismatches between documented safe modes and script behavior.

Mitigation: Review before installing, and avoid relying on list-models or environment-variable mode until the reported mismatches are fixed.

## Reference(s):

- [OpenClaw Alibaba Cloud Bailian Configuration](references/openclaw_alibaba_cloud.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or modify OpenClaw JSON configuration and backup files when the generated command or script is executed.]

## Skill Version(s):

0.1.4 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
