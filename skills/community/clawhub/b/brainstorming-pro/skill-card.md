## Description:

Facilitates structured ideation sessions for features, products, content, and strategy using goal clarification, divergent techniques, convergent prioritization, documentation, and follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arn0ld87](https://clawhub.ai/user/arn0ld87)

### License/Terms of Use:

MIT-0

## Use Case:

External users, facilitators, product teams, and developers use this skill to turn early ideas into structured session plans, prioritized concepts, design notes, and follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repository context during ideation, including files, docs, and recent commits.

Mitigation: Use it only where that context access is acceptable, and ask the agent to keep brainstorming in chat when sensitive repository material is present.

Risk: The skill may persist brainstorming output by writing a design document and committing it to git after ideation.

Mitigation: Require explicit approval before file creation, commits, recordings, worktree setup, or publishing session outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arn0ld87/skills/brainstorming-pro)
- [Facilitation Guide](references/facilitation-guide.md)
- [Brainstorming Techniques Deep-Dive](references/brainstorming-techniques.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown conversation, structured design sections, checklists, and optional design documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual German/English output; asks one question at a time and validates design sections incrementally.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
