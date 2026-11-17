## Description:

Deep Research Work is a comprehensive research framework that combines web search, content analysis, source verification, and iterative investigation to conduct in-depth research on any topic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiacode](https://clawhub.ai/user/jiacode)

### License/Terms of Use:


## Use Case:

Researchers, analysts, developers, and other external users use this skill to plan, gather, validate, synthesize, and report findings from multi-source investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included JavaScript workflow can generate mock sources and placeholder findings while the package presents itself as verified research.

Mitigation: Review outputs for real source URLs, citations, and provenance before relying on findings; treat the JavaScript as scaffold code unless it is changed to perform real retrieval and provenance tracking.

Risk: Sensitive research topics may be exposed through console logs or saved research files.

Mitigation: Avoid sensitive topics when logs or generated files may be retained, and review local retention practices before use.

## Reference(s):

- [Deep Research Skill README](artifact/README.md)
- [Deep Research Report Template](artifact/research_template.md)
- [ClawHub Skill Page](https://clawhub.ai/jiacode/skills/deepresearchwork)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research report with source attribution, confidence notes, limitations, and remaining questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured findings, source credibility assessment, contradictions or debates, and follow-up research areas.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
