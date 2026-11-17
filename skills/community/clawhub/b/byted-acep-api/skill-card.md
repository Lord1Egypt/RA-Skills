## Description:

Manages and troubleshoots authorized Volcengine Cloud Phone resources through a local Python CLI and OpenAPI client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operations teams use this skill to inspect and administer authorized Volcengine Cloud Phone test resources, including instances, resources, screenshots, tasks, apps, hosts, capacity, tags, DNS, routes, files, and device commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad destructive and privileged controls over authorized cloud-phone resources.

Mitigation: Use tightly scoped Volcengine credentials and require explicit user approval before state-changing operations such as create, delete, power, reboot, reset, install, uninstall, file transfer, or command execution.

Risk: Generic action calls and root command execution can perform high-impact operations outside routine workflows.

Mitigation: Review generic action-call requests carefully and avoid root command execution unless it is necessary for the authorized task.

Risk: File transfers and pre-signed edge URLs can expose sensitive data or access paths.

Mitigation: Treat transferred files, paths, and signed URLs as sensitive and avoid printing or sharing them unless the user explicitly requests it.

Risk: Resource subscription, renewal, and host operations can affect capacity or cost.

Mitigation: Confirm the product ID, resource type, data center, order history, and intended quantity before subscription, renewal, unsubscription, or host-level changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-acep-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, CLI arguments, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON parameter examples, file paths, and guidance for handling sensitive signed URLs and credentials.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
