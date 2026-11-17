## Description:

Safely check whether a Docker container's image has changed and, only when needed, recreate that docker run container with a user-provided original docker run command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to update containers managed by docker run while preserving a known recreate command and comparing Docker image Id values before recreation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can execute a user-provided recreate command through Bash on the host when apply mode is used.

Mitigation: Review the exact recreate command before use, run without --apply first, and use only commands you wrote and understand.

Risk: A recreate command may include risky Docker options or copied shell text.

Mitigation: Inspect for shell separators, command substitution, dangerous mounts, Docker socket access, --privileged, and --network host before approving apply mode.

Risk: Apply mode can remove the old container before recreation succeeds.

Mitigation: Confirm the full recreate command, prefer pinned image tags or digests for critical services, and review post-recreate state, health, and logs.

## Reference(s):

- [Command Parsing Notes](references/command-parsing.md)
- [ClawHub Skill Page](https://clawhub.ai/ugvfpdcuwfnh/skills/docker-container-rerun)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands; bundled script emits JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports container name, image, current and latest image Ids, whether recreation was needed, container state, health status, and recent logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
