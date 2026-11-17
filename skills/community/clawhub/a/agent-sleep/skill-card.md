## Description:

Agent Sleep helps agents consolidate memory, archive logs, clean workspaces, and optionally synchronize with CortexGraph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Agent Sleep to run or schedule maintenance cycles that summarize memory logs, archive daily notes, clean temporary files, and prepare optional CortexGraph synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises memory cleanup and scheduling behavior, which can affect workspace files if enabled without review.

Mitigation: Review exact archival, deletion, memory update, and scheduling behavior before installing or enabling automated runs.

Risk: The release includes an external note utility that can read and write an unrelated notes file outside the skill workspace.

Mitigation: Do not use or schedule the note utility unless the external path and data access are expected and documented.

Risk: Documented command paths and shipped files may not fully align, which can cause failed runs or unintended operator workarounds.

Mitigation: Confirm installed command paths and required memory directories before running sleep cycles.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guohongbin-git/skills/agent-sleep)
- [README](README.md)
- [Agent Instruction Manual](AGENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose scheduled runs and file-maintenance actions; execution should be reviewed before enabling automation.]

## Skill Version(s):

1.1.0 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
