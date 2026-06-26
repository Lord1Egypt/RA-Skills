## Description: <br>
BUDDY 宠物系统是一个虚拟宠物伴侣工具，用于生成、互动和展示 AI 宠物。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add a lightweight virtual pet companion that can hatch a pet, display pet cards, show petting animations, mute or unmute interactions, and provide a pet-aware assistant prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate on broad pet-related wording. <br>
Mitigation: Use explicit /buddy commands when tighter control is needed. <br>
Risk: The skill can print a pet-related context prompt for the assistant. <br>
Mitigation: Review the prompt output before relying on it in sensitive workflows. <br>
Risk: The skill stores small mute and saved-pet state in /tmp/buddy-state.json. <br>
Mitigation: Inspect or remove that file if local pet state should be reset. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxiaofeng0811-lgtm/buddy-pet) <br>
- [SKILL.md](SKILL.md) <br>
- [buddy.ts](scripts/buddy.ts) <br>
- [companion.ts](references/buddy/companion.ts) <br>
- [sprites.ts](references/buddy/sprites.ts) <br>
- [types.ts](references/buddy/types.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with ASCII art, command output, and short prompt guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist small mute and saved-pet state in /tmp/buddy-state.json] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
