## Description:

Diet Record logs meals from text descriptions or food photos, identifies food items, and estimates nutrition and calories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[734818028](https://clawhub.ai/user/734818028)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record meals, estimate calories and nutrition from photos or text, maintain diet preferences, and review daily intake summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can build a local history of sensitive diet and health-related details over time.

Mitigation: Use clear consent before logging and provide controls to review, correct, export, and delete diet records and preferences.

Risk: Diet history and preference files may be stored in the skill package directory when the artifact is used as written.

Mitigation: Store generated diet-log.jsonl and diet-preferences.json in a protected per-user data location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/734818028/skills/diet-record)
- [JSON Schema Draft 07](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown tables and summaries, JSONL meal records, JSON preference files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores diet history in diet-log.jsonl and user preferences in diet-preferences.json when used as written.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
