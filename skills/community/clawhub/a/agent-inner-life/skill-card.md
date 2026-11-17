## Description:

Keeps an agent's dated work state, evening journal, night reflections, and recall path, with a short native-memory summary injected into later sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dkistenev](https://clawhub.ai/user/dkistenev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill when they want an agent to keep a dated record of how work has been going, produce evening journal entries, perform optional night reflections, and read the record back on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally writes a cross-session native-memory summary that may appear in unrelated or shared-host sessions.

Mitigation: Use it only where native memory is isolated per user and workspace, and review summaries before saving them.

Risk: The local inner-life/ record and memory summary can persist after the skill is removed.

Mitigation: Delete inner-life/ and clear the memory summary when the record is no longer wanted.

Risk: Journaling work history can retain sensitive or personal details if the agent records too much.

Mitigation: Keep credentials, confidential material, and personal details out of summaries and prefer brief dated facts in local records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dkistenev/skills/agent-inner-life)
- [Project homepage](https://github.com/DKistenev/agent-inner-life)
- [State](references/state.md)
- [Journal](references/journal.md)
- [Recall](references/recall.md)
- [Dreams](references/dreams.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown files and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes under inner-life/ and refreshes a short native-memory summary during the evening routine.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
