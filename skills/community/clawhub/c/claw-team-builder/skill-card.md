## Description:

Helps OpenClaw users plan and create agent teams through guided requirement gathering, configuration analysis, conflict checks, workspace setup, bootstrap file generation, and OpenClaw configuration updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8421bit](https://clawhub.ai/user/8421bit)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to design additional agents, check for conflicts with existing OpenClaw settings, and generate the configuration, workspace directories, and bootstrap files needed to add those agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify the local OpenClaw configuration.

Mitigation: Review generated configuration paths and keep the automatic openclaw.json backup before accepting changes.

Risk: Channel credentials such as app secrets may be passed through command-line arguments.

Mitigation: Avoid entering production secrets on the command line when possible and prefer a protected secret-management workflow.

Risk: Validation and gateway commands such as openclaw doctor --fix and openclaw gateway restart can change local runtime state.

Mitigation: Run the workflow against a test OpenClaw configuration first and confirm the requested state-changing command before execution.

Risk: Bootstrap file generation depends on packaged template files.

Mitigation: Confirm the expected template files are present before relying on generated IDENTITY.md, SOUL.md, or USER.md output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/8421bit/skills/claw-team-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JavaScript helper scripts, and OpenClaw JSON configuration changes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local OpenClaw directories and bootstrap files and may update openclaw.json after user confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
