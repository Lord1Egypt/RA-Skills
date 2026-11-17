## Description:

Career Future Mirror collects career background, generates three differentiated career paths as an HTML report, supports a future-self dialogue, and creates an immersive future-letter HTML page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaniu001](https://clawhub.ai/user/shaniu001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and career-planning agents use this skill to collect career-stage details, analyze skill and resource gaps, compare three career paths, and generate Chinese-language planning reports and future-self letters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save sensitive career conversations, including resume details, employer history, salary goals, and personal career concerns.

Mitigation: Use only information the user is comfortable saving locally, avoid unnecessary identifying details, and review generated local files before sharing them.

Risk: Career background could be exposed through web searches.

Mitigation: Show and confirm search terms before searching, and remove identifying details from queries unless the user explicitly approves them.

Risk: Generated HTML reports may contact third-party CDNs when opened.

Mitigation: Open reports only in environments where remote font and script loading is acceptable, or review and replace remote assets before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaniu001/skills/career-future-mirror)
- [Career survey schema](artifact/reference/career_survey_data.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese Markdown dialogue, generated HTML reports, and JSON conversation data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML reports may load third-party CDN scripts when opened.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
