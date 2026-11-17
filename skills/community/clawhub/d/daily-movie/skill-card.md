## Description:

Daily movie and TV recommendation skill curated by genre, mood, or theme, with one suggested watch per day plus synopsis, streaming platform, and audience ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to get bilingual movie and TV recommendations by genre, mood, theme, ratings, and platform availability. Users can also enable scheduled morning and evening recommendation pushes for supported channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can schedule recurring direct-message pushes.

Mitigation: Enable push only for intended users and channels, review scheduled messages before deployment, and use the off command to remove scheduled pushes.

Risk: The skill adds a promotional star request to assistant replies.

Mitigation: Review the feedback prompt for the deployment context and remove or revise it if promotional messaging is not appropriate.

## Reference(s):

- [README](README.md)
- [ClawHub Daily Movie skill page](https://clawhub.ai/jiajiaoy/skills/daily-movie)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Bilingual Markdown recommendations with optional command-line scheduling output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include daily recommendation text, platform guidance, ratings, and recurring push setup or removal commands.]

## Skill Version(s):

1.0.4 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
