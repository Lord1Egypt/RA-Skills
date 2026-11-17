## Description:

Parses natural language visualization requests and recommends structured diagram schemes for Mermaid diagrams, ECharts-style charts, or image prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zatanyong](https://clawhub.ai/user/zatanyong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and external users use this skill to choose an appropriate diagram or chart representation from a natural language description and receive a structured recommendation with reasoning, alternatives, and confidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Mermaid or chart configuration may be inaccurate, unsupported by the target renderer, or misleading in production documents.

Mitigation: Review generated diagram code or chart configuration before using it in production documents.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured DiagramScheme-style JSON with optional Mermaid code, ECharts configuration, image prompts, reasoning, confidence, and clarification questions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include alternative diagram options ordered by preference and environment-aware fallback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
