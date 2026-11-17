## Description:

One advanced English word every day - IPA pronunciation, etymology, 3 example sentences, and quiz mode for GRE, SAT, IELTS, and C2 vocabulary practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and language-learning users use this skill to generate a daily advanced English vocabulary card with pronunciation, etymology, bilingual definitions, examples, and quiz practice. Users can also configure optional daily push reminders for supported chat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring push-notification scheduling can create repeated messages to external chat channels if push-toggle.js is run.

Mitigation: Run push-toggle.js only when recurring delivery is intended, and verify or remove cron entries after testing.

Risk: Generated cards are expected to use web search, write an HTML file, include Chinese translations, and contain an empty ad-ready area plus ClawCode footer branding.

Mitigation: Review generated HTML and vocabulary content before sharing or publishing, especially where branding, ads, or bilingual content need approval.

## Reference(s):

- [Daily Vocab on ClawHub](https://clawhub.ai/jiajiaoy/skills/daily-vocab)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with a generated single-file HTML vocabulary card and optional Node.js push-scheduling commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the vocabulary card to /mnt/user-data/outputs/daily-vocab.html when executed as described.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
