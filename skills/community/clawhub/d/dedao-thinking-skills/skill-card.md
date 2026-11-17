## Description:

A Chinese-language writing and thinking skill that routes user requests into six focused modes: polishing drafts, commenting on strengths, interrogating plans, reviewing records, creating channel-specific content, and generating cross-domain idea cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees can use this skill as a Chinese-language thinking and writing assistant for improving drafts, finding useful observations in notes, stress-testing plans, and turning ideas into publishable text. The skill is best suited for user-provided text, notes, drafts, or file paths that the user intentionally wants analyzed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide sensitive notes, drafts, or files for analysis.

Mitigation: Use pasted text for sensitive material when possible, and provide file paths only for documents intentionally meant to be read by the agent.

Risk: The skill can produce critique, retrospective analysis, or content drafts that may be mistaken for definitive advice.

Mitigation: Review generated outputs before acting on them or publishing them, especially when the source material is incomplete or high-stakes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/156554395/skills/dedao-thinking-skills)
- [Skill definition](artifact/SKILL.md)
- [Polish mode](artifact/polish.md)
- [Comment mode](artifact/comment.md)
- [Interrogate mode](artifact/interrogate.md)
- [Review mode](artifact/review.md)
- [Create mode](artifact/create.md)
- [Sprout mode](artifact/sprout.md)
- [Evaluation cases](artifact/evals.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses, depending on the selected mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are mode-specific and may include polished prose, commentary, critical review, retrospective analysis, channel-specific drafts, or a cross-domain idea card.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
