## Description: <br>
Helps OpenClaw users troubleshoot common plugin installation failures, including npm package-name errors, permission problems, and post-install verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dawai2005](https://clawhub.ai/user/dawai2005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose failed plugin installs, confirm correct npm package names, resolve common Windows/global npm permission issues, and verify installed tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package names or installation sources may be wrong or outdated, leading users to install the wrong npm package. <br>
Mitigation: Confirm package names and sources from official documentation before installing. <br>
Risk: Global npm installs or --force can overwrite or alter system-wide package state. <br>
Mitigation: Prefer normal npm install and permission-fix steps first; use global installs or --force only when the impact is understood. <br>


## Reference(s): <br>
- [ClawHub documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [npm Registry](https://www.npmjs.com/) <br>
- [ClawHub skill page](https://clawhub.ai/dawai2005/common-installation-troubleshooting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Troubleshooting advice is informational and should be checked against official package documentation before installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
