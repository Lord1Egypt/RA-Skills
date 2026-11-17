## Description:

Generates Chinese smart-home training data as JSONL multi-turn conversations from a tool name and a list of user instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaibuer](https://clawhub.ai/user/huaibuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and dataset curators use this skill to turn batches of Chinese smart-home user instructions into JSONL training conversations for tool-calling assistants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated examples may include household context or user instruction content that should not contain real personal data.

Mitigation: Use synthetic or anonymized household data and review generated JSONL before training.

Risk: Untrusted or malformed instruction lists can produce incorrect, misleading, or invalid training examples.

Mitigation: Validate the JSONL structure and tool-call fields before using generated data.

Risk: The generator writes to caller-selected output paths and may overwrite files.

Mitigation: Choose output paths deliberately and keep generated datasets under version control or backup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaibuer/skills/data-generator)
- [GreeQA tool requirements](references/tools/GreeQA.txt)
- [alarm_remind tool requirements](references/tools/alarm_remind.txt)
- [chat tool requirements](references/tools/chat.txt)
- [dev_control tool requirements](references/tools/dev_control.txt)
- [dev_info tool requirements](references/tools/dev_info.txt)
- [exit_dialog tool requirements](references/tools/exit_dialog.txt)
- [scene_control tool requirements](references/tools/scene_control.txt)
- [scene_generator tool requirements](references/tools/scene_generator.txt)
- [scene_guide tool requirements](references/tools/scene_guide.txt)
- [weather tool requirements](references/tools/weather.txt)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [JSONL files and plain-text generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each generated JSONL line is a single conversation object with fixed empty system and history fields.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
