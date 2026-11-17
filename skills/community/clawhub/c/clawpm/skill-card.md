## Description:

Clawpm provides multi-project task and research management through a JSON-first CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malphas-gh](https://clawhub.ai/user/malphas-gh)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Clawpm to manage project tasks, work logs, research notes, issues, and resumable project context across local workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned external GitHub CLI package that can change after review.

Mitigation: Review or pin the upstream clawpm package before installation.

Risk: The CLI creates persistent local project-management files and logs that may contain task notes, issue reports, blocker notes, research entries, or work-log summaries.

Mitigation: Avoid putting secrets or sensitive notes into Clawpm-managed records.

## Reference(s):

- [Clawpm homepage](https://github.com/malphas-gh/clawpm)
- [ClawHub skill page](https://clawhub.ai/malphas-gh/skills/clawpm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands emit JSON by default; use -f text for human-readable output.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
