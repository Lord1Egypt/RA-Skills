## Description:

Docker Manager helps agents inspect and administer Docker containers and images, including listing, starting, stopping, removing, monitoring resource usage, and viewing logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage Docker containers and images from an agent workflow, including inspection, logs, resource checks, lifecycle actions, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stop, delete, prune, or execute commands inside Docker containers without built-in confirmation.

Mitigation: Use it only on Docker hosts the agent is authorized to administer, confirm exact container, image, and volume targets before destructive actions, and avoid production hosts unless backups and rollback steps are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/docker-manager)
- [Publisher profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and docker binaries; actions operate on the Docker host available to the agent.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
