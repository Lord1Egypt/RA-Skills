## Description: <br>
Generate images using the internal Google Antigravity API (Gemini 3 Pro Image). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IPedrax](https://clawhub.ai/user/IPedrax) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate image files from text prompts through a Google Antigravity OAuth profile. It is intended for workflows that need native image generation without browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local Google Antigravity OAuth profile to authenticate requests. <br>
Mitigation: Install only when this credential use is intended, and review the selected auth profile before invoking the skill. <br>
Risk: User prompts are sent to a remote Google service without strong scoping or consent controls in the skill. <br>
Mitigation: Require user confirmation before generic image-generation requests and avoid prompts containing sensitive data. <br>
Risk: The remote endpoint or model response format may change, fail quota checks, or refuse a prompt. <br>
Mitigation: Handle failed runs by reviewing the script status text and model message before retrying or changing prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/IPedrax/antigravity-image-gen) <br>
- [Publisher profile](https://clawhub.ai/user/IPedrax) <br>
- [Google Antigravity API endpoint used by the skill](https://daily-cloudcode-pa.sandbox.googleapis.com/v1internal:streamGenerateContent?alt=sse) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, shell commands] <br>
**Output Format:** [PNG image file with stdout status text and a MEDIA path marker] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a required prompt, optional output path, and optional aspect ratio.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
