## Description:

Generates flowcharts, infographics, Gantt charts, and mind maps from natural language using EdrawMax AI APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xkweimeng](https://clawhub.ai/user/xkweimeng)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and external users use this skill to turn natural language descriptions into diagram assets and editable diagram source code for workflows, timelines, infographics, and knowledge maps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts are sent to an external diagram-generation service and may contain sensitive business, personal, or regulated information.

Mitigation: Disclose external processing before routine use and avoid submitting sensitive or regulated content unless the deployment has appropriate approval.

Risk: The downloader described in the artifact disables TLS certificate verification.

Mitigation: Keep TLS verification enabled and restrict network access to expected EdrawMax and storage hosts before using the downloader in routine workflows.

Risk: Downloaded PNG and SVG URLs are accepted without validation.

Mitigation: Validate URL hosts, file types, and response sizes before saving generated diagram files locally.

## Reference(s):

- [EdrawMax AI Skills API Reference](artifact/references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/xkweimeng/skills/build-diagram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown response with local PNG/SVG file paths, editable diagram source code, backup URLs, and JSON downloader output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may produce PNG and SVG diagram files downloaded from external URLs after API generation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
