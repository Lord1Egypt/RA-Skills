## Description:

Execution Harness helps agents navigate reliability patterns for completing Claude Code work, choosing hooks, preserving context, coordinating agents, recovering from errors, and verifying outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as a navigation entry point for an execution reliability suite covering persistent execution, tool governance, context memory, multi-agent coordination, error recovery, and quality verification. It routes users to specialized subskills rather than performing direct operations itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks can influence Claude Code sessions broadly.

Mitigation: Enable the package only in project-scoped settings and start with the minimal hook set needed for the task.

Risk: Session identifiers and state paths may be under-scoped.

Mitigation: Validate or sanitize session IDs and keep generated state inside a project-specific session directory.

Risk: Automated tmux recovery can send input to the wrong pane if scheduled too broadly.

Mitigation: Use the tmux recovery script only for allowlisted panes and avoid broad scheduled execution.

Risk: Diagnostics that invoke npx may install or run packages outside the local project toolchain.

Mitigation: Configure diagnostics to use already-installed local compilers or no-install mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/execution-harness)
- [Publisher profile](https://clawhub.ai/user/lanyasheng)
- [README](README.md)
- [Execution Harness architecture document](docs/ata-execution-harness-v4.md)
- [Design principles](principles.md)
- [Session state layout](shared/session-state-layout.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may direct the agent to subskills and hook scripts for concrete execution behavior.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter and subskill metadata report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
