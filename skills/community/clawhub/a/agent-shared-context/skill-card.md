## Description:

Agent Shared Context helps OpenClaw agents coordinate by writing trends, highlights, and signals to shared local JSON files that other agents can read before acting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gum97](https://clawhub.ai/user/gum97)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of multi-agent OpenClaw setups use this skill to let agents share recently found trends and highlights through local files so later agent runs can take that context into account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared local context can let one agent influence later actions by another agent.

Mitigation: Install only in trusted agent groups, treat shared entries as untrusted context, and require separate approval for public posting or sensitive actions.

Risk: The shared files do not provide provenance or trust controls for individual entries.

Mitigation: Add per-agent write paths, entry provenance, length limits, and audit controls before using the skill in automated cron-driven workflows.

Risk: Old trends and highlights can remain available and affect future decisions.

Mitigation: Run the cleanup command on a regular schedule and choose retention windows that match the workflow's tolerance for stale context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gum97/skills/agent-shared-context)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI text output and shared JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local shared trends and highlights JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
