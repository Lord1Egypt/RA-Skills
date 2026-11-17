## Description:

Professional-grade Chinese social media sentiment analysis report writer for government and enterprise use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangfromchu-ai](https://clawhub.ai/user/wangfromchu-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Government, enterprise, and institutional users use this skill to draft Chinese-language public opinion and sentiment analysis reports for social media or news events, including risk assessments, communication-data analysis, and actionable countermeasures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly defaults to Chinese formal institutional report conventions, which may be unsuitable for English, bilingual, or informal analysis requests.

Mitigation: Confirm the intended language, audience, and tone before using the generated report when the user needs a style outside the documented default.

Risk: Public-opinion reports can be misleading if incident facts, communication metrics, or source timestamps are incomplete or stale.

Mitigation: Require source attribution and dated communication data, separate confirmed facts from assumptions, and review conclusions before operational use.

Risk: The skill is intended for sensitive public-opinion and risk-assessment contexts where overly specific locations or actors may increase privacy or escalation risk.

Mitigation: Follow the artifact guidance to anonymize location references where appropriate and have sensitive reports reviewed by a responsible human decision-maker.

## Reference(s):

- [Report Type Templates & Formatting Standards](references/templates.md)
- [Aky Public Opinion on ClawHub](https://clawhub.ai/wangfromchu-ai/skills/aky-public-opinion)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown Chinese-language public opinion analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Formal Chinese official-document style; report length and structure vary by selected report type.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
