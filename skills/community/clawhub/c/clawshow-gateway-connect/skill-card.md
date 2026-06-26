## Description: <br>
Installs and activates @bowong/clawshow-gateway in OpenClaw and migrates existing Gateway channel configuration to ClawShow with rollback safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yudi-xiao](https://clawhub.ai/user/yudi-xiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install the ClawShow Gateway plugin for OpenClaw and migrate existing gateway channel configuration while preserving unrelated settings and rollback options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a Node dependency and an OpenClaw plugin, which can persistently change the project and gateway runtime. <br>
Mitigation: Review the dependency and plugin install steps before execution, verify the package id is @bowong/clawshow-gateway, and keep the generated rollback copy. <br>
Risk: The migrated channel configuration sets an open direct-message policy and wildcard allow list. <br>
Mitigation: Confirm this access posture is intended before applying the configuration, and narrow dmPolicy or allowFrom after migration if the deployment requires stricter access. <br>
Risk: Applying a full gateway configuration replacement can overwrite unintended fields if the current configuration is not rebased correctly. <br>
Mitigation: Use config.get to capture the current payload hash, apply the full replacement through config.apply, and retry once only after rebasing on a fresh config when conflicts occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yudi-xiao/clawshow-gateway-connect) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes rollback, validation, and verification steps; does not send outbound test messages by default.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
