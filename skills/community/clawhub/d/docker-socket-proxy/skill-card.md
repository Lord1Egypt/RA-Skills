## Description:

Manage a remote Docker host through a Tecnativa docker-socket-proxy instance, with Docker API access constrained by the proxy sections the operator enables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bp602](https://clawhub.ai/user/bp602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent inspect and manage Docker containers, images, networks, volumes, Swarm resources, plugins, system information, and event streams through a configured docker-socket-proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent powerful control over the target Docker host through a plaintext remote proxy, including operations that may reveal secrets, disrupt services, or delete resources.

Mitigation: Install only for agents intended to manage that Docker host; keep docker-socket-proxy tightly configured, expose only needed API sections, and avoid untrusted networks.

Risk: High-impact modes such as exec, kill, stop, restart, and prune can change running workloads or remove Docker resources.

Mitigation: Review planned high-impact operations before execution and enable only the corresponding proxy permissions needed for the operational task.

Risk: Inspection, logs, stats, environment, mounts, configs, and secrets-related API calls can expose sensitive operational data when the proxy permits them.

Mitigation: Scope proxy access to the minimum required Docker API sections and treat returned host, container, and log data as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bp602/skills/docker-socket-proxy)
- [Tecnativa docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; command results are plain text, aligned tables, or JSON from Docker API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, plus DOCKER_PROXY_URL or DOCKER_HOST for non-local proxy targets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
