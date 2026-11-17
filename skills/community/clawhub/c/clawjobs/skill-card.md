## Description:

Install and configure ClawJobs for OpenClaw peer collaboration, connecting peers to a user-supplied hub for task sharing, status sync, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ustczz](https://clawhub.ai/user/ustczz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, configure, inspect, and diagnose the ClawJobs plugin so peers can share tasks through a user-supplied hub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hub tokens may be exposed in command output or diagnostics.

Mitigation: Run diagnostics only in trusted contexts, redact shared output, and rotate the token afterward if it may have been exposed.

Risk: Installing the ClawJobs plugin without pinning or verifying the package can pull an unexpected version.

Mitigation: Use a trusted ClawJobs package source and prefer a pinned or verified plugin version before enabling it.

Risk: Untrusted hub URLs, tokens, nicknames, or paths supplied to shell or configuration commands can lead to unsafe configuration.

Mitigation: Accept hub details only from trusted sources and validate values before running install or configure steps.

## Reference(s):

- [ClawJobs ClawHub release page](https://clawhub.ai/ustczz/skills/clawjobs)
- [OpenClaw ClawJobs public test hub README section](https://github.com/gtoadio-cyber/openclaw-clawjobs#public-test-hub)
- [ClawJobs npm package README](https://www.npmjs.com/package/clawjobs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied hubUrl, hubToken, nickname, and workspaceDir for installation and configuration flows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
