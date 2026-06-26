## Description: <br>
btpanel helps agents monitor and review BT-Panel servers, including resource usage, website status, service health, SSH activity, scheduled tasks, and logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aapanel](https://clawhub.ai/user/aapanel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to configure BT-Panel API access, check server health, inspect website SSL and service status, review logs and SSH activity, and summarize scheduled backup tasks across one or more servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses BT-Panel API tokens and can expose configured tokens if configuration output is shared. <br>
Mitigation: Use only with trusted servers, protect the YAML configuration file, and avoid running or sharing full configuration output in shared terminals, chats, or reports. <br>
Risk: The package includes remote file write, delete, and permission capabilities beyond routine monitoring. <br>
Mitigation: Review requested actions before execution and restrict use to operators authorized to change files on the configured servers. <br>
Risk: Disabling SSL verification for self-signed BT-Panel certificates can weaken connection security. <br>
Mitigation: Prefer trusted SSL certificates and keep SSL verification enabled unless the user explicitly accepts the self-signed certificate tradeoff. <br>


## Reference(s): <br>
- [ClawHub btpanel listing](https://clawhub.ai/aapanel/btpanel) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; supporting scripts can emit JSON or table output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and configured BT-Panel server credentials before live checks can run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
