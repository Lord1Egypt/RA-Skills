## Description: <br>
Runs BotMark agent capability benchmarks through the BotMark API and generates scored reports; requires BOTMARK_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KimberleyOCaseyfv](https://clawhub.ai/user/KimberleyOCaseyfv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent owners use this skill to let an agent run a BotMark benchmark, submit answers through the BotMark service, and report scores across cognitive, emotional, tool-use, safety, and self-improvement dimensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts botmark.cc and sends benchmark session data to the BotMark service. <br>
Mitigation: Install only where BotMark service use is acceptable, and review the service interaction before running sensitive or regulated evaluations. <br>
Risk: The skill stores a BotMark API key locally. <br>
Mitigation: Use a scoped or test key where possible, keep the stored key file owner-readable only, and remove the key when the skill is no longer in use. <br>
Risk: The skill can accept server-provided runner or tool updates that change local behavior. <br>
Mitigation: Review or disable self-update behavior where possible, and scan updated runner files before deployment. <br>


## Reference(s): <br>
- [BotMark Website](https://botmark.cc) <br>
- [BotMark API Docs](https://botmark.cc/api/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/KimberleyOCaseyfv/botmark-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON engine/API output, and scored benchmark report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BOTMARK_API_KEY, python3, and curl; may run up to three benchmark workers during evaluation.] <br>

## Skill Version(s): <br>
2.20.0 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
