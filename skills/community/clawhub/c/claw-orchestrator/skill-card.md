## Description:

Orchestrates CC Agent analysis and file generation with WBClaw execution, preview, reporting, and memory updates for multi-step engineering tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenyang-x](https://clawhub.ai/user/zenyang-x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to split complex implementation work between a Claude Code analysis and generation step and a WBClaw execution step that validates outputs, previews HTML, writes a task report, and updates memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates user tasks to an external Claude CLI with broad read and write access in the configured WorkBuddy directory.

Mitigation: Run it only in a sandboxed workspace with limited files and review generated files before using or sharing them.

Risk: The documented workflow uses bypassed permission checks for file writing.

Mitigation: Prefer a version that removes bypassPermissions or requires explicit approval before file writes.

Risk: The script invokes a shell command around user-provided task text.

Mitigation: Prefer a version that avoids shell=True and passes command arguments without shell interpolation.

Risk: The skill depends on locally configured Node and Claude CLI paths.

Mitigation: Pin and verify the CLI or binary version before use, and treat missing or unexpected local paths as deployment blockers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zenyang-x/skills/claw-orchestrator)
- [ClawHub publisher profile](https://clawhub.ai/user/zenyang-x)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summaries, shell command examples, generated files, and task reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write deliverable files, task_report.md, and memory log entries in the configured WorkBuddy directory.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
