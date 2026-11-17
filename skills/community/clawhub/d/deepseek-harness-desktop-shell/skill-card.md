## Description:

This skill guides an agent through wrapping an already-running DeepSeek Harness Web UI on localhost into an Electron desktop application, covering prerequisites, a minimal shell, local URL loading, packaging, and scope boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potfromsky](https://clawhub.ai/user/potfromsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create a thin Electron desktop shell for a locally running DeepSeek Harness Web UI while preserving Harness functionality and plugin behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated Electron shell may trust a local Harness service or expose preload and IPC capabilities too broadly.

Mitigation: Authenticate or verify the local Harness service before loading it, restrict loading to the expected local origin, and keep preload and IPC APIs narrowly scoped and origin-checked.

Risk: The skill can lead an agent to install dependencies, scaffold files, and run packaging commands.

Mitigation: Review and modify the generated project before execution, pin Electron build dependencies with a lockfile, and obtain user confirmation before setup, packaging, or distribution steps.

Risk: Launch environment changes can affect the security posture of the local Harness process.

Mitigation: Preserve NODE_OPTIONS by default unless a reviewed environment-specific exception is required and documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/potfromsky/skills/deepseek-harness-desktop-shell)
- [Desktop shell prompt](artifact/references/desktop-shell-prompt.md)
- [DeepSeek Harness project referenced by artifact metadata](https://github.com/deepseek-ai/deepseek-harness)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets an already-running local DeepSeek Harness Web UI and expects human confirmation before high-impact setup, packaging, or distribution steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
