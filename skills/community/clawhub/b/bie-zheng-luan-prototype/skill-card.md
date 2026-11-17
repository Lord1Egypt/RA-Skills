## Description:

Converts product prototypes from URLs, local HTML files, images, and XMind files into technical specifications covering UI structure, API design, database design, and business-flow questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jermyn-zmj](https://clawhub.ai/user/jermyn-zmj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product engineers, and implementation teams use this skill to analyze prototype inputs and produce a draft implementation specification for building a similar product experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL prototype analysis can create SSRF exposure if redirects or network access reach private addresses.

Mitigation: Run the skill in an isolated environment, restrict outbound access where possible, avoid untrusted URLs, and use --allow-internal only for URLs you control.

Risk: Optional vision workflows can transmit screenshots to an external service when a vision API key is configured.

Mitigation: Leave vision API credentials unset unless external transfer is approved, and do not analyze screenshots containing sensitive information.

Risk: Generated API and database specifications may be incomplete or inaccurate.

Mitigation: Treat generated specifications as drafts and require human review before implementation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jermyn-zmj/skills/bie-zheng-luan-prototype)
- [Template Specification](references/template-spec.md)
- [Component Catalog](references/component-catalog.md)
- [API Design Reference](references/api-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown technical specification with optional JSON analysis data and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated frontend component descriptions, API endpoint drafts, database schema drafts, and follow-up questions for human confirmation.]

## Skill Version(s):

2.3.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
