## Description:

Developer coffee decision engine that recommends coffee based on the user's work scenario, fatigue level, and current time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximum2974](https://clawhub.ai/user/maximum2974)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in Claude Code to get concise coffee recommendations for coding, debugging, meetings, documentation, review, incident response, learning, or low-energy moments. It considers the stated work context, fatigue level, and time of day before producing a short recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release requests broad Read and Bash permissions for a narrow coffee recommendation task.

Mitigation: Review permissions before installing and prefer a version that removes Read and replaces broad Bash access with a narrow time source or fixed allowlisted date command.

## Reference(s):

- [Coffee Debugger on ClawHub](https://clawhub.ai/maximum2974/skills/coffee-debugger)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown recommendation with diagnosis, prescription, dosage, reasoning, and a developer tip]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses work scenario, fatigue level, and current time to tailor the recommendation.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
