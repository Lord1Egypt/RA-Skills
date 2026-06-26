## Description: <br>
Documents 1Panel server administration APIs for website, container, database, file, backup, host, and system management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breadbot86](https://clawhub.ai/user/breadbot86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to look up 1Panel API endpoints and compose authenticated requests for server administration tasks across websites, containers, databases, backups, files, hosts, and settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents broad 1Panel administration APIs that can affect websites, containers, databases, files, backups, hosts, SSH settings, scripts, and system settings. <br>
Mitigation: Install it only for agents that are expected to work with a privileged 1Panel server API, and require explicit human approval before any high-impact operation is executed. <br>
Risk: API key exposure could allow unauthorized access to the managed 1Panel server. <br>
Mitigation: Store the API key as a secret, avoid placing it in prompts or logs, rotate it if exposed, and prefer least-privilege access where 1Panel configuration allows it. <br>
Risk: Network transport or endpoint mistakes could send administrative requests to an unsafe or unintended server. <br>
Mitigation: Use HTTPS or a trusted private network and verify the target 1Panel address before composing or approving requests. <br>
Risk: Documented destructive actions include deletes, overwrites, restores, reboot/shutdown, SSH access, shell or script execution, private-key handling, and broad file or database operations. <br>
Mitigation: Require confirmation of target IDs, paths, hostnames, and payloads before running these operations, and keep backups available before changes that affect persistent data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/breadbot86/1panel-api) <br>
- [1Panel website](https://1panel.cn/) <br>
- [1Panel documentation](https://1panel.cn/docs/) <br>
- [1Panel GitHub repository](https://github.com/1Panel-dev/1Panel) <br>
- [1Panel Docker Hub image](https://hub.docker.com/r/1panel/1panel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API endpoint descriptions, request parameters, JSON examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; generated requests may target privileged 1Panel administration APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
