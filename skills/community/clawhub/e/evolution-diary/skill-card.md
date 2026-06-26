## Description: <br>
个人进化追踪系统 — 不是冷冰冰的数据，是你的成长伴侣。记录心流、低谷、习惯、情绪，让每一次进化都有温度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexduming](https://clawhub.ai/user/alexduming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal growth companion for tracking flow moments, low points, habits, mood scores, achievements, and weekly reflection letters. It helps structure local journaling and reflective check-ins in a warm, human-facing style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal mood, habit, low-point, and reflection data in a local plaintext JSON file. <br>
Mitigation: Install only if local plaintext storage is acceptable, review or delete ~/.openclaw/data/evolution档案.json periodically, and avoid recording sensitive details that should not remain on disk. <br>
Risk: Automatic flow or low-point detection may suggest saving inferred personal state from conversation context. <br>
Mitigation: Use explicit commands and confirm before saving entries; disable automatic detection in configuration when manual-only tracking is preferred. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexduming/evolution-diary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown responses with JSON data records and occasional shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local plaintext JSON under ~/.openclaw/data and read optional configuration from ~/.openclaw/config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
