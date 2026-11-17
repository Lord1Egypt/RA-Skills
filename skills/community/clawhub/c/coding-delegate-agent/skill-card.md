## Description:

Delegate coding tasks to Codex, Claude Code, or Pi agents via background process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate coding, review, refactoring, and app-building tasks to background coding agents while managing execution mode, workspace isolation, and session monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to launch other coding agents with broad file, command, network, and repository authority.

Mitigation: Install and run it only in disposable worktrees or containers, with explicit review of the spawned agent's intended scope.

Risk: The skill describes bypassed approval and unsandboxed execution modes.

Mitigation: Avoid bypass and yolo-style modes unless that level of authority is intentionally approved for the workspace.

Risk: Delegated coding workflows may perform repository actions such as commits, pushes, PR comments, or package installs.

Mitigation: Review generated changes and commands before any commit, push, PR comment, or global package installation.

Risk: Untrusted issue text or prompts could be copied into shell commands.

Mitigation: Do not paste untrusted text directly into executable shell commands; quote, sanitize, or summarize it first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utromaya-code/skills/coding-delegate-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for launching and monitoring coding agents; no structured machine-readable output is specified.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
