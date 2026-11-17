## Description:

Set up and maintain automatic OpenClaw and skill updates on Windows, macOS, and Linux, with Windows-native Git Bash guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo220yuyaodog](https://clawhub.ai/user/leo220yuyaodog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, run, verify, and summarize recurring OpenClaw and installed-skill updates. It is especially relevant for Windows environments that need native shell execution and Git Bash checks instead of WSL paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring no-input updates can modify OpenClaw and all installed skills through unpinned command execution.

Mitigation: Use automated updates only intentionally; prefer a pinned ClawHub CLI version, a trusted registry or verified local binary, and a review step before bulk updates.

Risk: Scheduled update jobs can continue applying changes after the initial setup.

Mitigation: Keep the schedule conservative, deliver concise run summaries, and maintain a documented way to disable the job or roll back updates.

Risk: On Windows, the wrong bash executable can route build steps through WSL instead of the expected native Git Bash/MSYS environment.

Mitigation: Verify `where.exe bash` and `bash --version` before update execution, and prioritize Git Bash/MSYS in PATH for build steps that require bash.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leo220yuyaodog/skills/auto-updater-windows)
- [Agent Implementation Guide](references/agent-guide.md)
- [Update Summary Examples](references/summary-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline PowerShell and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise update summaries covering updated, unchanged, and failed items.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
