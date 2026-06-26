## Description: <br>
Controls Dot e-ink display devices by checking status, listing content, pushing text or images, and switching displayed content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnqxu](https://clawhub.ai/user/johnqxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Dot e-ink display users use this skill to check device status, manage display content, push text or processed images, and advance to the next content item through the Dot API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses DOT_API_KEY to query and update a user's Dot display. <br>
Mitigation: Treat DOT_API_KEY as a credential, keep it out of shared logs or prompts, and install the skill only when device control is intended. <br>
Risk: Text, images, and links sent through the Dot API may be displayed on the device or transmitted to the Dot service. <br>
Mitigation: Confirm the intended content before asking the agent to push or switch display items, and avoid private content that should not be displayed or transmitted. <br>
Risk: Image pushes depend on local image conversion before the API request. <br>
Mitigation: Use trusted local image files and a trusted ImageMagick installation when preparing images for the display. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnqxu/dot-eprint-controller) <br>
- [Dot API service](https://dot.mindreset.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DOT_API_KEY, DOT_DEVICE_ID, curl, and ImageMagick convert for image pushes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
