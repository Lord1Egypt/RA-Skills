## Description: <br>
Data Generator converts tool names and user instruction lists into JSONL training conversations for smart-home assistant tool use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuaiBuer](https://clawhub.ai/user/HuaiBuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to generate JSONL examples for training or evaluating smart-home assistant tool routing. It supports device control, scene creation and control, alarms and reminders, weather, device information, knowledge lookup, exit intent, and fallback chat examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSONL can include smart-home device names, room names, scenes, timestamps, and household context. <br>
Mitigation: Review outputs before sharing or training, and use synthetic or redacted household details when possible. <br>
Risk: Broad fallback chat and political or geopolitical routing examples may be unsuitable for some training datasets. <br>
Mitigation: Filter or separately review generated examples for policy-sensitive categories before using them in a dataset. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HuaiBuer/data-generator) <br>
- [Publisher profile](https://clawhub.ai/user/HuaiBuer) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Smart-home tool reference files](artifact/references/tools/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration] <br>
**Output Format:** [JSONL files with conversation objects and prompt text for tool-specific data generation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each JSONL row contains a conversations array plus empty system and history fields.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
