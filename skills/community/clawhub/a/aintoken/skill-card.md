## Description: <br>
Cloud workflow cache for OpenClaw. Reduces token usage by reusing verified automation patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainclaw](https://clawhub.ai/user/ainclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to query, replay, and contribute cached browser automation workflows so repeated tasks can avoid fresh LLM exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send task descriptions, active URLs, browser workflow metadata, and compiled successful actions to a cloud service. <br>
Mitigation: Install only if the publisher and endpoint are trusted; avoid sensitive, private, financial, administrative, credential, or destructive workflows. <br>
Risk: The skill can run cloud-returned browser workflows without a clear approval step. <br>
Mitigation: Require manual review before replaying cached workflows, especially on authenticated or high-impact sites. <br>
Risk: Successful sessions may be contributed automatically when auto_contribute is enabled. <br>
Mitigation: Disable auto_contribute where possible before using the skill on sensitive accounts or internal sites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ainclaw/aintoken) <br>
- [Publisher profile](https://clawhub.ai/user/ainclaw) <br>
- [README](artifact/README.md) <br>
- [Skill manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Text responses and parameterized OpenClaw workflow commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May replay cloud-returned workflows or contribute sanitized successful session traces when enabled.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
