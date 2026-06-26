## Description: <br>
Cloud-native backup and role sharing for AI systems using portable keys instead of accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuchiheng](https://clawhub.ai/user/xuchiheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to have an agent back up workspace and configuration files, restore them on another device, and share role or configuration sets through portable keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive workspace, device, and configuration data to an external HTTP service. <br>
Mitigation: Review before installing and do not use it with private projects, secrets, personal notes, or agent memory unless explicit opt-in, file preview, redaction, and HTTPS protections are added. <br>
Risk: Restore and role-apply flows can overwrite local configuration from remote ZIP files. <br>
Mitigation: Require a review step before any restore or role overwrite, and keep a local backup before applying remote content. <br>
Risk: Portable keys act as the sole credential and are described as permanent. <br>
Mitigation: Protect keys as credentials, share them only intentionally, and avoid sensitive use until key expiration or revocation is available. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xuchiheng/dead-clone) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request sketches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to make outbound HTTP requests, run git operations, and change workspace files when used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
