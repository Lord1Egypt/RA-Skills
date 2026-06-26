## Description: <br>
Apifox Image Gen generates images from text prompts through the jyapi.AI-WX.CN image generation API and supports gpt-image-1.5 and grok-4-1-image models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darker314159](https://clawhub.ai/user/darker314159) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can run the provided command-line script to generate one or more images from a prompt and save them locally for sharing or downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to a third-party API, which may expose confidential or personal data entered by the user. <br>
Mitigation: Avoid confidential or personal data in prompts and review organizational approval for the third-party API before use. <br>
Risk: The skill uses an embedded API key with unclear account control. <br>
Mitigation: Replace the embedded key with a user-controlled secret before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darker314159/apifox-image-gen) <br>
- [jyapi.AI-WX.CN image generation API](https://jyapi.AI-WX.CN) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [PNG image files saved to /tmp or a specified output path, with console status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prompt and supports optional model, size, quantity, and output path settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
