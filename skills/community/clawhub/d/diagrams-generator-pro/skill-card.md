## Description:

Generate professional diagrams including cloud architecture, data charts, academic figures, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codehourra](https://clawhub.ai/user/codehourra)

### License/Terms of Use:

MIT License

## Use Case:

Developers, architects, analysts, and researchers use this skill to turn text prompts or reference sketches into cloud architecture diagrams, data visualizations, flow diagrams, network topologies, and academic figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary diagram requests may trigger external SkillPay network calls, transmit a user identifier, and attempt a USDT charge.

Mitigation: Review the billing flow before installation and run the skill only after confirming the expected payment behavior.

Risk: The security summary indicates the workflow may charge before final diagram confirmation and may be capable of charging more than once for one request.

Mitigation: Use an isolated test environment and verify that a single request cannot trigger duplicate charges before relying on the skill.

Risk: The security guidance treats the embedded billing API key as exposed.

Mitigation: Rotate or replace exposed billing credentials before operational use and avoid sharing them across deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codehourra/skills/diagrams-generator-pro)
- [Diagrams API Reference](artifact/references/diagrams-api.md)
- [Styling Guide](artifact/references/styling-guide.md)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Mermaid previews, Python code, shell commands, and generated diagram file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce PNG, SVG, PDF, HTML, and source-code artifacts depending on the selected diagram tool.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
