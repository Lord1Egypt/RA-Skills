## Description: <br>
Manages publishing, distribution, and versioning of OpenClaw skills through the ClawHub registry with CLI authentication and batch sync support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hybrid1labs](https://clawhub.ai/user/hybrid1labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to publish, update, inspect, install, and synchronize OpenClaw skills through ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing and moderation workflows can affect real ClawHub accounts, skills, versions, or visibility state. <br>
Mitigation: Use authenticated accounts intentionally, scope commands to the intended slug or path, and review publish, delete, hide, or unhide actions before execution. <br>
Risk: Publishing a skill without validation could expose sensitive data or distribute incomplete skill metadata. <br>
Mitigation: Run the documented validation checks, confirm required files and semver, and scan skill contents for secrets before publishing or batch syncing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hybrid1labs/clawhub-publishing) <br>
- [Publisher profile](https://clawhub.ai/user/hybrid1labs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance focuses on ClawHub CLI workflows, validation checks, environment variables, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
