## Description: <br>
A first aid learning assistant for first aid concepts, CPR, bleeding control, wound care, fractures, bandaging, kit building, and simulated emergency practice, with boundaries against real-time emergency guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[futureidiot](https://clawhub.ai/user/futureidiot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to learn first aid concepts, practice simulated response scenarios, configure first aid kits, correct common myths, and manage optional daily tips. It is not for active emergencies or diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may try to apply educational first-aid content during an active emergency. <br>
Mitigation: Install and present the skill only as an educational aid, and preserve the artifact's emergency boundary that redirects real emergencies to emergency services. <br>
Risk: Daily tips create recurring messages and may not include the usual emergency disclaimer. <br>
Mitigation: Make the recurring schedule visible to the user, provide a disable path, and avoid treating daily tips as emergency instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/futureidiot/first-aid-kit) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown text with optional JSON-shaped daily tip scheduling configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses begin with an educational safety notice except for configured daily tips, which the artifact says may omit the notice.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
