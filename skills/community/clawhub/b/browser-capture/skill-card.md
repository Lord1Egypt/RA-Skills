## Description: <br>
Captures webpage screenshots and real content images with OpenClaw Browser while filtering out icons, logos, avatars, buttons, and other small UI imagery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n0nsense11](https://clawhub.ai/user/n0nsense11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide OpenClaw Browser workflows for finding, inspecting, and saving webpage screenshots or high-quality content images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to open webpages, inspect image elements, click page controls, and save browser screenshots or image downloads locally. <br>
Mitigation: Use it only on intended sites, avoid sensitive logged-in pages unless explicitly authorized, and confirm browser actions before running them. <br>
Risk: Download and copy commands can save remote content locally or write to the wrong path. <br>
Mitigation: Review image URLs, curl commands, and output paths before execution. <br>
Risk: Proxy services may expose browsing activity or access targets without appropriate permission. <br>
Mitigation: Use proxy services only when explicitly trusted and authorized for the target site. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n0nsense11/browser-capture) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and locally saved image or screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save screenshots under ~/.openclaw/media/browser/ or image files to user-selected workspace paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
