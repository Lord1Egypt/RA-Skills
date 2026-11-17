## Description:

Data Generator / 数据生成器 generates JSONL training data from user instructions, a tool name, and command lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaibuer](https://clawhub.ai/user/huaibuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dataset builders use this skill to generate JSONL conversation training samples from command lists for supported tool-call scenarios such as smart-home control, reminders, weather, and chat fallback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and command data are sent to the configured LLM endpoint.

Mitigation: Do not provide confidential commands or datasets unless the configured API_URL endpoint is trusted.

Risk: The documented npx install command is unpinned.

Mitigation: Install from a trusted ClawHub/npm environment and pin installer or package versions in controlled workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaibuer/skills/data-generator-waai)
- [Publisher profile](https://clawhub.ai/user/huaibuer)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [JSONL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each record contains conversation turns and system context; generation depends on the configured LLM endpoint.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
