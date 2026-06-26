## Description: <br>
Generate images using ChatGPT/DALL-E through OpenClaw browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonim1](https://clawhub.ai/user/sonim1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to guide an agent through ChatGPT web image generation from an already logged-in browser session, including tab discovery, prompt submission, waiting for generation, and downloading results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates an already logged-in ChatGPT browser tab and can submit prompts, inspect visible page state, click controls, and download files through the user's account. <br>
Mitigation: Use a dedicated browser profile or isolated ChatGPT session, verify the attached tab before actions, and detach or close the tab when finished. <br>
Risk: The security summary flags the skill as suspicious because it presents use of a real browser session as bypassing bot detection. <br>
Mitigation: Review the workflow before installing and confirm that this browser-control behavior is acceptable for the intended account, workspace, and terms of use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an attached browser tab with an active ChatGPT session and OpenClaw browser relay access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
