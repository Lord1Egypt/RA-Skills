## Description:

Generates commercial complex market research reports in Word, HTML presentation, and editable PPTX formats from project location, site parameters, and current market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxarch1980](https://clawhub.ai/user/dxarch1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare commercial real-estate market research for project approval, positioning analysis, competitor research, tenant mix planning, and financial modeling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses external search services and may share project locations or market-research prompts with third-party services.

Mitigation: Avoid confidential addresses and non-public deal data unless external lookups are approved.

Risk: The skill can rely on browser access to Xiaohongshu through a Chrome remote debugging session.

Mitigation: Use a dedicated browser profile and avoid exposing a normal logged-in Chrome profile through remote debugging.

Risk: The security summary flags unsafe output file generation.

Mitigation: Generate files only in a dedicated output folder with trusted project names until path and HTML escaping are fixed.

Risk: Market, rent, cap rate, and valuation data may be stale, incomplete, or estimated.

Mitigation: Keep the skill's source-date labels, mark missing values as pending, and review financial assumptions before using reports for decisions.

## Reference(s):

- [Skill page](https://clawhub.ai/dxarch1980/skills/commercial-market-report)
- [Chapter writing guide](references/chapters.md)
- [Data source guide](references/data-sources.md)
- [Word report format guide](references/report-format.md)
- [PPT format guide](references/ppt-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated DOCX, HTML, and PPTX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports include charts, tables, financial estimates, source notes, and presentation slides.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
