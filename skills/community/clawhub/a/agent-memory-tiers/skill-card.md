## Description:

Agent Memory Tiers gives OpenClaw agents persistent tiered workspace memory through L0 state snapshots and L1 rolling context files so activations can start with current state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dirtyrootsstudio](https://clawhub.ai/user/dirtyrootsstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add compact, self-updating memory files to OpenClaw agent workspaces so agents can resume work, track blockers, and coordinate across multi-agent swarms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent workspace memory can retain secrets, credentials, private user data, or sensitive business details if agents write them into L0/L1 files.

Mitigation: Keep L0/L1 summaries short and explicitly exclude secrets, credentials, private user data, and sensitive business details from memory files.

Risk: Stale or oversized memory files can mislead agents or erode the token savings the skill is intended to provide.

Mitigation: Keep L0 to exactly four lines, keep L1 to the seven most recent daily entries, update current state rather than appending logs, and remove resolved blockers promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dirtyrootsstudio/skills/agent-memory-tiers)
- [Publisher profile](https://clawhub.ai/user/dirtyrootsstudio)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown templates and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces L0.md and L1.md memory templates plus agent instruction snippets; no code execution or network behavior is required.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
