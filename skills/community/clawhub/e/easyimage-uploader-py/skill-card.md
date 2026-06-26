## Description: <br>
Uploads local image files to an EasyImages 2.0 service and returns a hosted image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fm7077](https://clawhub.ai/user/fm7077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to upload an existing local image to an EasyImages 2.0 instance and receive a shareable hosted URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EasyImages upload tokens and delete URLs are sensitive and could grant upload or deletion capability if exposed. <br>
Mitigation: Keep config.json private, avoid echoing configured tokens, and share delete URLs only when the user explicitly asks for deletion capability. <br>
Risk: The security scan reported unsandboxed review-helper behavior and possible exposure of diffs to external reviewer tools. <br>
Mitigation: Install only in a trusted maintainer environment and avoid reviewer-tool modes that may send private code, secrets, or unreleased work to external services. <br>


## Reference(s): <br>
- [EasyImages 2.0 API notes](references/api.md) <br>
- [EasyImages2.0 upstream project](https://github.com/icret/EasyImages2.0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with optional shell commands and JSON upload results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the direct hosted image URL as the main result; thumbnail and delete URLs are handled only when useful or explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
