## Description: <br>
COSER模卡生成器cosercard-skill helps agents create professional cosplay and model display cards from user photos with automated layouts, style selection, profile information, and export options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zaosusu](https://clawhub.ai/user/Zaosusu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cosplay creators, models, photographers, and agents use this skill to generate photo-based casting or profile cards in multiple layouts and export sizes for social sharing, printing, or portfolio use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store local generation history in learning_data.json, including metadata about card generation. <br>
Mitigation: Delete learning_data.json when local usage history should not be retained. <br>
Risk: Contact details, exact location, body measurements, and social handles entered by the user may appear on generated cards. <br>
Mitigation: Enter only information intended for the final card and review generated images before sharing or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zaosusu/cosercard-skill) <br>
- [Pillow documentation](https://python-pillow.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated cards are image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports wide, mobile, square, A4, banner, and landscape card outputs; local usage history may be written to learning_data.json.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
