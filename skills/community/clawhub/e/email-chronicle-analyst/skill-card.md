## Description:

Deeply analyzes long-running, multi-party, multi-thread email records by filtering social noise, reconstructing event progression, identifying decision points, and presenting execution actions and open items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinsuzc](https://clawhub.ai/user/kevinsuzc)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and project managers use this skill to turn messy email chains into concise project chronologies, responsibility assignments, decision records, risks, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive email contents may be written to a predictable shared temporary file during .eml preprocessing.

Mitigation: Use a per-run private temporary file or in-memory processing, restrict access to cleaned email text, and delete extracted text after analysis.

Risk: Email analysis may produce incorrect responsibility assignments, decision summaries, or next-step recommendations if source messages are incomplete or ambiguous.

Mitigation: Review the generated chronology and action list against the original emails before using it for project follow-up or escalation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinsuzc/skills/email-chronicle-analyst)
- [Publisher profile](https://clawhub.ai/user/kevinsuzc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report with tables, status labels, timelines, decisions, open items, and prioritized action recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For .eml inputs, the skill instructs the agent to preprocess email into cleaned plain text before analysis.]

## Skill Version(s):

4.3.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
