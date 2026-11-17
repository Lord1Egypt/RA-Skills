## Description:

Clawng Term Memory helps OpenClaw agents persist and restore core knowledge by version-controlling memory files and pushing changes to a private Git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidharket](https://clawhub.ai/user/davidharket)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to preserve agent identity, memory, operating rules, and installed skills across machines through Git-backed commits and pushes. It also supports reviewing history, diffing memory files, reverting previous versions, and aggregating per-machine memories for synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push sensitive agent state and core knowledge files to a remote Git repository.

Mitigation: Review memory files before enabling the skill, use a private repository, and configure least-privilege credentials.

Risk: The merge workflow aggregates and displays memory content from all configured agent branches.

Mitigation: Run the merge workflow only when cross-agent memory aggregation is intended and the configured remote is trusted.

Risk: Stored Git credentials could expose repository access if the workspace is compromised.

Mitigation: Prefer SSH or a secure credential manager and avoid git credential.helper store.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidharket/skills/clawng-term-memory)
- [Publisher profile](https://clawhub.ai/user/davidharket)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May commit selected agent memory and skill files, push to an agent-specific Git branch, and print aggregated memory content during merge collection.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
