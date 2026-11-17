## Description:

1Panel API Skills provides API reference guidance for managing websites, containers, databases, files, backups, jobs, hosts, settings, and related modules on a 1Panel server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breadbot86](https://clawhub.ai/user/breadbot86)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to look up 1Panel API endpoints and prepare authenticated requests for routine Linux server administration tasks. It is intended for work with trusted 1Panel instances where the agent may help manage infrastructure resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports broad server administration workflows, including destructive or host-level changes.

Mitigation: Require explicit confirmation before deleting files or databases, changing SSH, firewall, Docker, or Nginx settings, partitioning disks, running scripts, or creating persistent services.

Risk: 1Panel API keys and generated tokens grant administrative access to the managed server.

Mitigation: Use HTTPS or WSS connections, treat API keys and tokens as administrator credentials, and avoid sharing production secrets unless required for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/breadbot86/skills/1panel-api)
- [1Panel official website](https://1panel.cn/)
- [1Panel documentation](https://1panel.cn/docs/)
- [1Panel GitHub repository](https://github.com/1Panel-dev/1Panel)
- [1Panel Docker Hub image](https://hub.docker.com/r/1panel/1panel)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with API endpoint descriptions, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for authenticated 1Panel API operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
