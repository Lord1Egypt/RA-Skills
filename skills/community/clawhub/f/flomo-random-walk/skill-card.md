## Description:

Flomo Random Walk starts from a random Flomo note, surfaces related notes, and helps users build an exploratory knowledge-walk path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayshna](https://clawhub.ai/user/jayshna)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to explore their Flomo memo collection by starting from a random note, reviewing recommended related notes, selecting follow-up notes, and ending with a recorded walk path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published instructions expose a Flomo API token.

Mitigation: Do not install this version until the exposed token has been removed and revoked; use a user-provided secret from a protected store instead.

Risk: The skill stores note-walk history locally, which may reveal personal note metadata or exploration patterns.

Mitigation: Clearly explain what history is saved, where it is stored, and provide a way to disable or delete that history.

## Reference(s):

- [Flomo MCP endpoint](https://flomoapp.com/mcp)
- [ClawHub skill page](https://clawhub.ai/jayshna/skills/flomo-random-walk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Flomo MCP calls and may record walk history locally when run by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
