## Description: <br>
Guides an agent through collaborative brainstorming before creative or coding work by clarifying intent, exploring alternatives, and turning ideas into validated design notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlreal](https://clawhub.ai/user/tlreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to structure early-stage product, feature, component, and behavior-change discussions before implementation. It helps convert vague requests into scoped design sections, options, constraints, success criteria, and implementation handoff material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger too broadly for routine creative or coding work. <br>
Mitigation: Review the trigger description before installation and narrow activation conditions if routine work should not enter a brainstorming workflow. <br>
Risk: The artifact behavior includes writing design documents and committing them to git. <br>
Mitigation: Require explicit user approval before file writes or git commits. <br>
Risk: The source instructions are primarily in Chinese, which may be hard for some reviewers to audit. <br>
Mitigation: Translate and review the instructions before deployment when Chinese is not the reviewer's working language. <br>


## Reference(s): <br>
- [Core Brainstorming on ClawHub](https://clawhub.ai/tlreal/core-brainstorming) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Conversational text and Markdown design notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose options, ask one focused question at a time, and draft design documentation after user validation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
