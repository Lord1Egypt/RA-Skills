## Description:

Creates and switches OpenClaw agents, including generated workspace files, default capabilities, and configuration updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tevfikgulep](https://clawhub.ai/user/tevfikgulep)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to create named agents, generate their workspace files, and switch or route tasks between agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent workspaces and global OpenClaw configuration changes may alter the host environment.

Mitigation: Review the generated files and config update path before installation, and back up the OpenClaw config before running the script.

Risk: Crafted agent IDs or names may corrupt files or execute commands because of input-handling flaws.

Mitigation: Do not allow untrusted users or prompts to choose agent IDs or names until sed templating and post-sanitization ID validation are fixed.

Risk: The generated USER.md contains a hardcoded user identity.

Mitigation: Replace the hardcoded identity with deployment-specific user information before distribution or use.

Risk: Predictable temporary file handling can be unsafe in shared or untrusted environments.

Mitigation: Patch the script to use secure temporary file creation before running it outside a controlled single-user environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tevfikgulep/skills/agent-factory)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell command examples, and generated OpenClaw configuration entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent OpenClaw agent workspace files and appends an agent entry to the OpenClaw config.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
