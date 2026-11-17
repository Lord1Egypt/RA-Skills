## Description:

Guides agents through source-building, launching, and troubleshooting DeepSeek Harness on Windows, including managed Node, pnpm, workspace persistence, symlink, and port 3080 pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potfromsky](https://clawhub.ai/user/potfromsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, build, launch, and troubleshoot DeepSeek Harness on Windows. It is especially relevant for managed Node environments where sandbox hooks, pnpm path handling, stale symlinks, and port conflicts can affect startup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact local troubleshooting steps could affect the wrong environment, process, or file if applied broadly.

Mitigation: Require user confirmation and scope actions to the documented Harness target: clear NODE_OPTIONS only for the dsh web launch, stop only the port-3080 Harness process, and delete only the stale symlink under ~/.dsh.

Risk: Some guidance is specific to Windows, managed Node, or WorkBuddy/CodeBuddy sandbox behavior.

Mitigation: Confirm the runtime and operating system before use, and adapt or skip sandbox-specific steps outside those environments.

## Reference(s):

- [Detailed Windows deployment pitfalls](references/deploy-pitfalls.md)
- [English README](README.en.md)
- [DeepSeek Harness repository](https://github.com/deepseek-ai/deepseek-harness)
- [ClawHub skill page](https://clawhub.ai/potfromsky/skills/deepseek-harness-windows-deploy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on Windows 10/11 and scopes high-impact troubleshooting steps to DeepSeek Harness tasks.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
