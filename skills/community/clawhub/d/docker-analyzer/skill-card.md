## Description:

A tool for exploring layers in a Docker image and inspecting local Docker image and container metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Docker images, containers, layers, history, disk usage, compose files, and optimization opportunities in a local Docker environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optimize command can let a crafted image name run arbitrary local code.

Mitigation: Use only in a low-privilege environment and avoid passing untrusted image names, especially to optimize, until the issue is fixed.

Risk: The skill reads Docker image and container metadata from the local Docker environment.

Mitigation: Run it only where access to local Docker metadata is appropriate for the user and workload.

## Reference(s):

- [Docker Analyzer ClawHub skill page](https://clawhub.ai/xueyetianya/skills/docker-analyzer)
- [xueyetianya ClawHub publisher profile](https://clawhub.ai/user/xueyetianya)
- [wagoodman/dive reference project](https://github.com/wagoodman/dive)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read Docker image and container metadata from the local Docker environment.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
