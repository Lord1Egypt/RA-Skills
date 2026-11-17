## Description:

Generate flowcharts, infographics, Gantt charts, and mind maps from natural language using EdrawMax AI APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

Proprietary Software License

## Use Case:

Developers and external users use this skill to turn natural language prompts into diagrams, including process flows, infographics, project timelines, and mind maps. The skill calls EdrawMax-operated services and presents generated image files plus editable source code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram prompts and generated artifacts are sent to EdrawMax-operated remote services.

Mitigation: Avoid confidential, regulated, customer, roadmap, or other sensitive content unless the deployment has explicit approval for this data flow.

Risk: The skill automatically downloads remote PNG and SVG files after generation.

Mitigation: Review or harden downloader behavior before sensitive use, including redirect handling, exact host allowlisting, file size limits, and PNG/SVG validation.

## Reference(s):

- [EdrawMax AI Skills API Reference](references/api-reference.md)
- [ClawHub skill listing](https://clawhub.ai/wondershare-boop/skills/edrawmax-skills)

## Skill Output:

**Output Type(s):** [API Calls, Files, Markdown, Code, Shell commands]

**Output Format:** [Markdown with local PNG/SVG file paths and diagram source code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads generated PNG and SVG artifacts locally when EdrawMax returns trusted HTTPS URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
