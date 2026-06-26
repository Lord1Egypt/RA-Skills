## Description: <br>
Generate ASCII art from text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate text-based ASCII art in OpenCode-compatible workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may cause the skill to activate in busy agent environments. <br>
Mitigation: Tighten the trigger set before deployment and keep activation scoped to explicit ASCII art requests. <br>
Risk: The skill references a local capability_executor.py dependency. <br>
Mitigation: Install only in environments where the referenced local executor is trusted and controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/generate-ascii-art) <br>
- [ASCII image converter reference](https://www.bilibili.com/video/BV19R22YyEuz) <br>
- [ASCII art tools reference](https://www.bilibili.com/video/BV1TP4y1a73U) <br>
- [ASCII text and image conversion reference](https://www.bilibili.com/video/BV16myLYwEKT) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Plain text ASCII art, with optional Markdown or code examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local capability executor when available; no persistence or credential handling is indicated by the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
