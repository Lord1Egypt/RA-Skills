## Description: <br>
Automates Doubao AI image creation by connecting to a browser or API session, submitting prompts, extracting generated image URLs, and saving images locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangm199](https://clawhub.ai/user/huangm199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to drive Doubao image generation workflows, collect generated image URLs, and download results with less manual browser interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct authenticated API use relies on saved cookies and can act as the user account without manual browser interaction. <br>
Mitigation: Use a dedicated Doubao account or browser profile and require explicit approval before any browserless API call uses saved cookies. <br>
Risk: Referenced Node scripts are not present in the reviewed artifact, so their behavior cannot be confirmed from the release files. <br>
Mitigation: Review the missing Node scripts before installation and confirm exactly which cookie file is read and where images are saved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangm199/doubao-image-auto) <br>
- [Doubao image creation page](https://www.doubao.com/chat/create-image) <br>
- [Doubao](https://www.doubao.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown with JavaScript and PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce image URLs and downloaded image files when executed by an agent with browser, network, and local filesystem access.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
