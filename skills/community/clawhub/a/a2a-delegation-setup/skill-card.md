## Description:

Guided setup and troubleshooting for installing, enabling, configuring, verifying, and updating @aramisfa/openclaw-a2a-outbound in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aramisfacchinetti](https://clawhub.ai/user/aramisfacchinetti)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install, configure, enable, verify, update, and troubleshoot the @aramisfa/openclaw-a2a-outbound plugin on an OpenClaw Gateway host before handing off to routine remote-agent delegation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides installation of a third-party OpenClaw plugin, so the package must be trusted before use.

Mitigation: Confirm trust in @aramisfa/openclaw-a2a-outbound, prefer a reviewed pinned version, and test updates before production use.

Risk: Enabling the plugin changes persistent OpenClaw Gateway behavior.

Mitigation: Run the Gateway with least privilege and review configuration changes before applying install, update, restart, or config edit commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aramisfacchinetti/skills/a2a-delegation-setup)
- [openclaw-a2a-outbound README](https://github.com/aramisfacchinetti/openclaw-a2a-plugins/tree/master/packages/openclaw-a2a-outbound#readme)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and text command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup checks, configuration paths, verification steps, and handoff guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
