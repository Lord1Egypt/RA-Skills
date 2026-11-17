## Description:

Condenses scattered chat messages, notes, or logs into a concise structured daily standup summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, team leads, and developers use this skill to turn raw chat exports, notes, or pasted messages into a structured daily standup summary with completed work, planned work, and blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated summaries may be inaccurate for ambiguous, multilingual, or unusually formatted chat logs.

Mitigation: Review and adjust generated summaries before sharing them with a team or adding them to meeting notes.

Risk: Untrusted input logs may contain Markdown links, images, or formatting that could mislead readers when copied into the output.

Mitigation: Inspect generated Markdown for unexpected links or formatting before publishing it.

Risk: The helper script reads local files selected by the user.

Mitigation: Run it only on intended chat logs or notes and avoid including sensitive content that is not needed for the standup.

## Reference(s):

- [Standup Formatting Reference](references/formatting.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON standup summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are grouped into completed, planned, and blockers sections with contributor attribution when parsed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
