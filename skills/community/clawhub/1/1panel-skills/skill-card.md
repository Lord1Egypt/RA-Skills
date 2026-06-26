## Description: <br>
1Panel operation skill for agent runtimes. Use when the user wants an assistant to interact with a 1Panel instance for resource monitoring, websites, certificates, app status, container status, logs, cronjobs, task-center records, node-management status, and future management actions. The current implementation focuses on query and inspection interfaces and keeps module-grouped mutation definitions reserved for later expansion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1panel](https://clawhub.ai/user/1panel) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
Developers and operations teams use this skill to let an agent inspect and troubleshoot a reachable 1Panel instance through authenticated API calls. It supports monitoring, websites, applications, containers, logs, cronjobs, task-center records, and node status, with mutation definitions reserved for intentional future expansion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unrestricted signed request command can reach 1Panel admin API operations beyond the skill's normal inspection workflows. <br>
Mitigation: Use a least-privilege API key, restrict source IPs, and avoid raw request or sign commands unless privileged debugging is explicitly required. <br>
Risk: The skill requires sensitive 1Panel API credentials. <br>
Mitigation: Store credentials only in the runtime secret environment, rotate them regularly, and do not commit real API keys into source control. <br>
Risk: Disabling TLS verification can expose API credentials and responses to interception. <br>
Mitigation: Use HTTPS with certificate validation enabled and avoid setting ONEPANEL_SKIP_TLS_VERIFY except in controlled test environments. <br>


## Reference(s): <br>
- [Module Groups](references/module-groups.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable 1Panel instance and API credentials supplied through environment variables or CLI flags.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
