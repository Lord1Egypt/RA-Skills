## Description:

Maintains persistent focus on active work with hierarchical task tracking that captures decisions, TODOs, constraints, blockers, and sub-agent status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noquant](https://clawhub.ai/user/noquant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Focus Tree to keep active project state in local focus files, resume after context compaction, and track current TODOs, blockers, decisions, and handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes and updates local focus files that can influence how an agent resumes work.

Mitigation: Review FOCUS.md and FOCUS-LOG.md periodically and keep their contents limited to current project state.

Risk: Untrusted pasted task text may be carried into focus context.

Mitigation: Review task text before adding it to focus files and avoid storing sensitive or untrusted instructions as authoritative context.

Risk: Archiving or clearing focus state may remove context that is still needed.

Mitigation: Confirm the current work is complete or intentionally paused before archiving or clearing focus state.

## Reference(s):

- [Focus Tree ClawHub release page](https://clawhub.ai/noquant/skills/focus-tree)
- [Focus Tree project homepage](https://github.com/openclaw/focus-tree)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown focus-state files with optional CLI command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates local FOCUS.md and FOCUS-LOG.md files in the active workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
