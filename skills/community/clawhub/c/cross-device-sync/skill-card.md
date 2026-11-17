## Description:

This skill helps OpenClaw users synchronize memory files across devices through a private GitHub repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coreyleung-art](https://clawhub.ai/user/coreyleung-art)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to set up GitHub-backed synchronization for OpenClaw memory files across multiple devices. It generates setup, sync, status, and configuration guidance for maintaining shared memory data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub tokens may be exposed during setup or command execution.

Mitigation: Use only a private repository you control, use a fine-grained low-scope token, rotate tokens regularly, and review credential handling before running setup.

Risk: Untrusted repository URLs or credentials may affect shell command execution.

Mitigation: Do not run setup with untrusted repository URLs or tokens until command construction and input handling have been reviewed and fixed.

Risk: Workspace contents may be uploaded broadly to GitHub.

Mitigation: Assume synchronized workspace files can be uploaded, review exclusions before syncing, and use a private repository with minimal access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coreyleung-art/skills/cross-device-sync)
- [Publisher profile](https://clawhub.ai/user/coreyleung-art)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with JavaScript and Bash command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local synchronization scripts and setup/status guidance for GitHub-backed OpenClaw memory sync.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, config.json, RELEASE_NOTES.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
