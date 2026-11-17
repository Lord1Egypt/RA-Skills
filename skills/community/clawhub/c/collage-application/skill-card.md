## Description:

Guides Chinese Gaokao applicants through college application planning based on province, selected subjects, score, rank, and intended majors, then generates a visual application sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ym9zep](https://clawhub.ai/user/ym9zep)

### License/Terms of Use:

MIT-0

## Use Case:

External students, families, and admissions advisors use this skill to collect and validate Gaokao application inputs, confirm normalized values, generate a visual application plan, and continue with admissions-related questions after the sheet is created.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Student application data may be sent to an external UAT service without documented retention, operator, or consent details.

Mitigation: Disclose the external processing before use and proceed only when the user accepts that processing and the missing retention and operator details.

Risk: The workflow may ask users to provide an API key in chat if environment-based configuration is unavailable.

Mitigation: Use a trusted secret mechanism such as WENXIANG_API_KEY and do not paste API keys into chat.

Risk: Generated college application guidance may be incorrect, incomplete, or unsuitable for a high-stakes admissions decision.

Mitigation: Review generated plans and recommendations against official admissions materials before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ym9zep/skills/collage-application)
- [External UAT application generation API](https://wxc-college-uat.randomlife.cn/v1/collage_application/create)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or text responses with script command invocations and a generated image URL when successful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include normalized JSON-like input data and a URL for the generated visual application sheet.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
