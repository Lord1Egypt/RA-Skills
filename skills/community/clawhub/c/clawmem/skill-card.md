## Description:

Bootstrap, repair, and verify the ClawMem OpenClaw plugin. Use when ClawMem is not yet installed, not selected as the active memory plugin, missing per-agent provisioning, or needs setup troubleshooting. After activation, rely on the bundled `clawmem` plugin skill for everyday recall, saving, schema, collaboration, mental-model guidance, communication, and manual memory operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianthereal](https://clawhub.ai/user/ianthereal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, activate, verify, and repair the ClawMem memory plugin, including active memory-slot selection, per-agent provisioning, and non-interactive read-access checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party memory plugin and makes it OpenClaw's active memory provider.

Mitigation: Install only if the publisher is trusted, prefer a pinned and reviewed package version, and verify package provenance when possible.

Risk: Verification steps can expose a provisioned token through shell variables or shared command output.

Mitigation: Avoid sharing shell logs from verification steps and rotate the provisioned token if it may have been exposed.

## Reference(s):

- [ClawMem ClawHub skill page](https://clawhub.ai/ianthereal/skills/clawmem)
- [ClawMem API endpoint](https://git.clawmem.ai/api/v3)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with shell, Python, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, verification, repair, and compatibility guidance for OpenClaw and ClawMem.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
