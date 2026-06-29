## Description: <br>
Manages an OpenClaw agent avatar by accepting an image or URL, or by searching Freepik for candidate vector avatars, then saving the selected image and updating the avatar reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to replace an agent avatar from a supplied image, image URL, or Freepik search candidate while keeping the OpenClaw workspace avatar path and IDENTITY.md in sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist a Freepik API key in TOOLS.md. <br>
Mitigation: Prefer an environment variable or dedicated secret store; delete or rotate any key written to TOOLS.md if it may have been exposed. <br>
Risk: The skill makes lasting OpenClaw avatar and identity changes. <br>
Mitigation: Review the selected image and target agent before applying the change, and keep the previous IDENTITY.md avatar path available for rollback. <br>
Risk: The skill sends search requests to Freepik and downloads third-party image assets. <br>
Mitigation: Avoid sensitive details in search prompts and review the selected asset and applicable Freepik terms before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/songhonglei/agent-avatar-manager) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Freepik API key dashboard](https://www.freepik.com/developers/dashboard/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Freepik API, download avatar images, persist a Freepik API key, and update OpenClaw identity files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
