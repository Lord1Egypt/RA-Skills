## Description:

Astra Docker lets an agent execute commands and read or write files in Astra's /workspace directory inside the astra-env Docker container.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walniek](https://clawhub.ai/user/walniek)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to work inside an existing Astra Docker workspace, run shell commands, and create or update files in the container workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad sudo-backed Docker command and file-write access can exceed the intended container boundary.

Mitigation: Install only when the agent is expected to control astra-env, remove sudo where possible, restrict paths to /workspace, and require clear confirmation for destructive commands and writes.

Risk: Shell-built Docker commands can expose command, path, or content parameters to injection.

Mitigation: Replace shell-built command strings with structured Docker calls and validate command, working directory, file path, and file content inputs before execution.

## Reference(s):

- [Astra Docker ClawHub listing](https://clawhub.ai/walniek/skills/astra-docker)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration]

**Output Format:** [Text responses and command output from Docker workspace operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the astra-env container with /workspace as the default working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
