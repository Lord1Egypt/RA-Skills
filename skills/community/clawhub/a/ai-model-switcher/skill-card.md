## Description:

AI模型切换器 helps OpenClaw users choose between local and cloud AI models by task type to balance cost and performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[savidwilbert](https://clawhub.ai/user/savidwilbert)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to inspect model options, select task-specific local or cloud model modes, generate model-switch commands, and review usage or cost statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud model modes may route future prompts or documents to external model providers after the user applies the generated OpenClaw model change.

Mitigation: Review the selected provider and task type before applying a generated model-switch command, especially for sensitive prompts or documents.

Risk: Local switch logs and statistics can expose model usage metadata on shared machines.

Mitigation: Review the skill configuration and disable switch logging when local usage metadata should not be retained.

Risk: The inspected script appears incomplete and generates manual switch commands rather than providing fully automatic switching.

Mitigation: Treat the skill as a model-selection and command-generation helper, and verify model changes in OpenClaw after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/savidwilbert/skills/ai-model-switcher)
- [Publisher profile](https://clawhub.ai/user/savidwilbert)
- [Usage documentation](docs/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text with suggested OpenClaw commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local switch logs and usage statistics when logging is enabled.]

## Skill Version(s):

1.0.0 (source: ClawHub release, skill metadata, config/config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
