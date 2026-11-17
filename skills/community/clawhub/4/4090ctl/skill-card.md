## Description:

Remotely manage a 4090 server over SSH to monitor Docker containers, restart Dify services, and check system status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olmmlo-cmd](https://clawhub.ai/user/olmmlo-cmd)

### License/Terms of Use:


## Use Case:

Developers or operators authorized to administer the referenced 4090 server use this skill to retrieve SSH and Docker commands for status checks, logs, resource monitoring, and Dify service restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes ready-to-run SSH and Docker restart commands for a specific server.

Mitigation: Install and use it only in environments where the user is authorized to administer that server, and require explicit confirmation before running restart commands.

Risk: Commands use the configured SSH identity and can access service logs or host resource information.

Mitigation: Confirm the target host and SSH identity before execution; prefer read-only status and log commands unless a disruptive action is requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olmmlo-cmd/skills/4090ctl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash code blocks and a service table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes administrative SSH and Docker commands that may affect running services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
