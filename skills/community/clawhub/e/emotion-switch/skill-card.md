## Description: <br>
Emotion switch lets users set an assistant's persistent emotional tone and 1-5 intensity for the current conversation while distinguishing those commands from the user's own emotional disclosures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npccxx](https://clawhub.ai/user/npccxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and conversational agent users use this skill to keep a Chinese-oriented assistant in a user-selected emotional speaking style until the user switches or resets it. It is intended for style control in normal dialogue, not for overriding safety, urgent, or serious user needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally sustains a non-neutral assistant tone, which may be inappropriate where strict neutrality, language mirroring, or explicit style disclosure is required. <br>
Mitigation: Use or enable it only in contexts where emotional tone shifting is desired; constrain or avoid it in neutral, compliance-sensitive, or disclosure-sensitive workflows. <br>
Risk: High-intensity emotional styles, especially anger or frustration, could make responses feel confrontational if applied without restraint. <br>
Mitigation: Keep safety and serious user needs above style instructions, cap extreme intensity outside creative contexts, and preserve the artifact rule against insulting, threatening, manipulating, or mocking the user. <br>


## Reference(s): <br>
- [Emotion guide](references/emotion-guide.md) <br>
- [Emotion intensity examples](references/emotion-intensity-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/npccxx/emotion-switch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Natural-language conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only style behavior; no code execution, data access, or external connections.] <br>

## Skill Version(s): <br>
1.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
