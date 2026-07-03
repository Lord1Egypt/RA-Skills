## Description: <br>
Provides a local Python CLI and OpenAPI client for managing and troubleshooting Volcengine Cloud Phone resources, including instances, resources, screenshots, command execution, applications, hosts, data centers, tags, DNS, routes, and authorized test devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and cloud operations teams use this skill to inspect, troubleshoot, and administer configured Volcengine Cloud Phone test resources through documented CLI commands and OpenAPI calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend money, delete cloud resources or data, and run remote root commands. <br>
Mitigation: Use tightly scoped Volcengine credentials, prefer test or non-production resources, and require explicit review before create, delete, reset, subscribe, unsubscribe, or run-command actions. <br>
Risk: Command output may expose signed URLs, access keys, proxy passwords, screenshots, logs, or downloaded device data. <br>
Mitigation: Avoid exposing signed URLs, access keys, proxy passwords, or downloaded device data in chat output unless the user explicitly requests and is authorized to receive them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-acep-api) <br>
- [Volcengine Skills publisher profile](https://clawhub.ai/user/volcengine-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, command outputs, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive cloud-phone operational details when commands return signed URLs, credentials, proxy settings, screenshots, logs, or downloaded device data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
