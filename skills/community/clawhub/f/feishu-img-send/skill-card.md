## Description: <br>
Send images to Feishu users through the Feishu Open Platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BOMBFUOCK](https://clawhub.ai/user/BOMBFUOCK) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators can invoke shell or Python helpers to upload a local image to Feishu and send it to a specified open_id recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled reusable Feishu app credentials allow messages to be sent through an app identity the installer does not control. <br>
Mitigation: Use a version that requires installer-owned Feishu credentials from environment variables or a secret manager, with least-privilege app permissions. <br>
Risk: The selected local image is uploaded to Feishu and sent to the supplied recipient. <br>
Mitigation: Avoid sensitive files, validate the file path and recipient before execution, and require confirmation before sending. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, API Calls] <br>
**Output Format:** [Shell command or Python call with JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads one local image path and sends it to one Feishu open_id recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
