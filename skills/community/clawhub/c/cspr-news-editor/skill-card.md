## Description:

Rank cspr candidate items and write a concise personalized Markdown newspaper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happywalkers](https://clawhub.ai/user/happywalkers)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn CSPR candidate news items into a ranked, personalized Markdown newspaper with recommendation reasons and discovery-route notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a CSPR profile and feedback history while preparing personalized recommendations.

Mitigation: Install and run it only where that app-specific state is appropriate for news personalization.

Risk: The skill saves shown links so future runs can avoid repeats.

Mitigation: Use the intended CSPR home and review saved newspaper state according to the user's retention expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happywalkers/skills/cspr-news-editor)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown newspaper with JSON ranking metadata and blocker notes when publishing should stop]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CSPR profile, feedback history, candidate items, seen URLs, and discovery-route metadata to support ranking and repeat filtering.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
