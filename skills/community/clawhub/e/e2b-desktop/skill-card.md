## Description:

Control E2B Desktop sandboxes for computer-use agents, including sandbox lifecycle management, screenshots, mouse and keyboard actions, command execution, and VNC streaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyhn](https://clawhub.ai/user/eyhn)

### License/Terms of Use:


## Use Case:

Developers and computer-use agent builders use this skill to operate an E2B-hosted Linux desktop sandbox through shell wrappers for lifecycle control, screen capture, input actions, application launch, URL opening, streaming, and sandbox-side commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell wrapper arguments may allow injected local Python code when values are built from untrusted or raw model-generated strings.

Mitigation: Review commands before execution, avoid passing untrusted strings directly to scripts, and run the skill only in an isolated environment.

Risk: VNC streaming is unauthenticated by default.

Mitigation: Prefer authenticated streaming and avoid displaying secrets or sensitive data in the sandbox desktop.

Risk: The e2b-desktop dependency is installed at runtime by users.

Mitigation: Pin and review the dependency before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eyhn/skills/e2b-desktop)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts return plain text status, environment-style values, command output, stream URLs, or PNG screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires E2B_API_KEY; sandbox state may be stored in ~/.e2b_state unless E2B_SANDBOX_ID is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
