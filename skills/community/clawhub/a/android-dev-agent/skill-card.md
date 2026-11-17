## Description:

Assists with AOSP builds, HAL analysis, Android Framework changes, ROM customization, and SDK/NDK troubleshooting using isolated work areas and written reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happysurfingeveryday-art](https://clawhub.ai/user/happysurfingeveryday-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate Android platform build issues, analyze HAL and Framework changes, customize ROMs, and produce patches or reports for source-level Android work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Android source syncs and builds can consume substantial disk, network, and CPU resources.

Mitigation: Run the skill in an environment sized for AOSP work and monitor build directories, network use, and long-running commands.

Risk: Generated patches or source-change recommendations may affect Android platform behavior.

Mitigation: Review proposed patches and reports before applying them, then test changes against the intended Android version and target device.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/happysurfingeveryday-art/skills/android-dev-agent)
- [Publisher Profile](https://clawhub.ai/user/happysurfingeveryday-art)
- [Android Platform Manifest](https://android.googlesource.com/platform/manifest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with command logs, analysis, patch guidance, and code or configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are named under memory/reports/android-dev-*.md and may reference isolated worktrees under memory/worktrees/android-{task-id}/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
