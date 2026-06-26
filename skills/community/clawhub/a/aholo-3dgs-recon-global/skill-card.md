## Description: <br>
Aholo OpenAPI v1 global 3D tasks for reconstruction and generation: upload media, create a world task, and check or poll worldId status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohao17501671450-lgtm](https://clawhub.ai/user/xiaohao17501671450-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and 3D content teams use this skill to submit videos or image sets to Aholo services for 3DGS reconstruction, create prompt or image based 3D generation tasks, and retrieve task status and result links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images, videos, and an Aholo API key to Aholo services. <br>
Mitigation: Use only media and credentials approved for Aholo processing, and confirm the account and destination before creating tasks. <br>
Risk: The release evidence reports that HTTPS certificate verification is disabled by default. <br>
Mitigation: Enable TLS verification before running, for example with AHOLO_FORCE_SSL_VERIFY=1. <br>
Risk: The release evidence reports use of a beta API endpoint that does not match the documented gateway. <br>
Mitigation: Confirm that api-beta.aholo3d.com is an intended endpoint for the account before uploading sensitive media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohao17501671450-lgtm/aholo-3dgs-recon-global) <br>
- [Aholo API keys](https://labs.aholo3d.com/api-keys) <br>
- [Aholo quickstart](https://labs.aholo3d.com/quickstart) <br>
- [Aholo Studio 3DGS viewer](https://studio.aholo3d.com/3dgs-model/{worldId}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status messages with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns worldId values, viewer links, polling summaries, result file links, and actionable error messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
