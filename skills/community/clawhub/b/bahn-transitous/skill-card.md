## Description:

Search Deutsche Bahn train connections with a local bahn-cli tool backed by Transitous.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bone187](https://clawhub.ai/user/bone187)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to run local bahn-cli searches for German rail connections, departure times, platforms, durations, changes, and train numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs node index.js from a local ~/Code/bahn-cli directory, so an unintended local checkout could run the wrong code.

Mitigation: Before installing or using the skill, confirm that ~/Code/bahn-cli contains the intended Deutsche Bahn CLI code.

Risk: The skill is scoped to German rail lookups and may be unsuitable for broader travel planning.

Mitigation: Use it for German rail connection searches, not hotel, flight, or full itinerary planning.

## Reference(s):

- [Transitous](https://transitous.org/)
- [ClawHub Skill Page](https://clawhub.ai/bone187/skills/bahn-transitous)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise rail-search summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on a local ~/Code/bahn-cli checkout and Transitous service availability.]

## Skill Version(s):

2.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
