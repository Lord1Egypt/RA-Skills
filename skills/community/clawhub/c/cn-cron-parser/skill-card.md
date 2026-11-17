## Description:

Parses five-field cron expressions into Chinese human-readable descriptions, shows common templates, and can calculate upcoming run times with croniter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators working in Chinese use this skill to interpret five-field cron schedules, review common cron templates, and optionally compute upcoming execution times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional next-run feature depends on the external croniter package.

Mitigation: Install dependencies in a virtual environment and pin or review the croniter version when supply-chain control matters.

Risk: The helper is intended for Chinese-language cron interpretation and may not cover every scheduler-specific cron variant.

Mitigation: Use it for five-field cron expressions and review generated descriptions or next-run times against the target scheduler before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-cron-parser)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and Chinese-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional next-run calculations require croniter; normal responses are concise Chinese-language cron explanations.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
