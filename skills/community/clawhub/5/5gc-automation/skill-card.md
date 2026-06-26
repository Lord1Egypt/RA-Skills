## Description: <br>
Automates 5GC web dashboard workflows for adding and editing network functions and configuring PCF policy chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei120](https://clawhub.ai/user/liuwei120) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Telecom lab engineers and developers use this skill to automate 5GC dashboard configuration for AMF, UDM/AUSF, SMF, UPF, gNB, UE, PCF, NRF, QoS, Traffic Control, PCC, and SMPolicy resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes shared dashboard credentials. <br>
Mitigation: Rotate the exposed credentials and require per-user or vault-provided credentials before use. <br>
Risk: Reusable browser sessions may remain on disk. <br>
Mitigation: Protect or disable session caching and clear cached sessions after controlled runs. <br>
Risk: Automation can make live 5GC dashboard configuration changes. <br>
Mitigation: Run only in controlled lab or trusted internal environments, and add confirmation, dry-run, and rollback procedures before shared or production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuwei120/5gc-automation) <br>
- [Publisher profile](https://clawhub.ai/user/liuwei120) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can modify the selected 5GC dashboard project and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
