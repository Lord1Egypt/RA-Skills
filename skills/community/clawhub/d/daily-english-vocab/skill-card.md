## Description:

Daily English Vocab provides scheduled English vocabulary and conversation practice, delivering daily small-talk phrases and themed word lessons with pronunciation, examples, and learning tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forkercat](https://clawhub.ai/user/forkercat)

### License/Terms of Use:

MIT-0

## Use Case:

External English learners, especially Chinese speakers in English-speaking countries, use this skill to schedule daily bite-sized American English lessons with small-talk practice and rotating vocabulary categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron delivery can send lessons to the wrong channel or at the wrong time if schedule, timezone, channel, or recipient settings are incorrect.

Mitigation: Review the cron time, timezone, channel, recipient chat ID, and explanation language before enabling delivery.

## Reference(s):

- [Vocabulary Categories](references/categories.md)
- [ClawHub Skill Page](https://clawhub.ai/forkercat/skills/daily-english-vocab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown lesson content with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use memory/english-vocab-state.json to track category rotation and avoid repeated words.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
