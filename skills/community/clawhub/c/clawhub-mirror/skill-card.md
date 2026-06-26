## Description: <br>
ClawHub镜像源管理技能。智能选择最佳镜像源，优先国内镜像，需要时使用VPN访问国外源。解决国内访问速度慢的问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xixiaohe](https://clawhub.ai/user/xixiaohe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to select and persist a faster ClawHub mirror configuration, especially when local network conditions make the default service slow or unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can redirect future ClawHub traffic and skill operations to alternate mirror or registry domains. <br>
Mitigation: Inspect the configured mirror list before running it, use only trusted endpoints, and reset CLAWHUB_SITE and CLAWHUB_REGISTRY if traffic should return to the default service. <br>
Risk: Persisted mirror configuration or shell loader files may continue affecting later ClawHub sessions. <br>
Mitigation: Avoid adding generated loaders to shell profiles until the endpoint is trusted, and remove ~/.clawhub mirror configuration when the mirror is no longer intended. <br>
Risk: The setup documentation references PowerShell scripts that are not present in the provided artifact, while the artifact contains Python configuration scripts. <br>
Mitigation: Review the available artifact scripts directly and run only commands that match files present in the installed skill. <br>


## Reference(s): <br>
- [ClawHub Mirror release page](https://clawhub.ai/xixiaohe/clawhub-mirror) <br>
- [xixiaohe publisher profile](https://clawhub.ai/user/xixiaohe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write ClawHub mirror configuration under the user's home directory and set CLAWHUB_SITE and CLAWHUB_REGISTRY for the current process.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
