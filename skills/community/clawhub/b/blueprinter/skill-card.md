## Description:

Blueprinter helps agents generate architecture diagrams, system diagrams, flowcharts, and technical specification sheets as flat blueprint-style HTML/CSS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yofine](https://clawhub.ai/user/yofine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and technical writers use this skill to ask an agent for flat, high data-ink HTML/CSS diagrams for architectures, systems, flowcharts, and specification sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML/CSS diagrams may contain incorrect or misleading technical details if the prompt or source architecture is incomplete.

Mitigation: Review diagrams against the relevant architecture, system design, or specification before publishing or using them for implementation decisions.

Risk: The bundled HTML template includes a Google Fonts link, which may load third-party resources.

Mitigation: Replace or remove the external font link when diagrams must avoid third-party font loading.

Risk: The bundled HTML template defaults the document language to English.

Mitigation: Update the HTML language attribute when producing diagrams for another locale.

## Reference(s):

- [Blueprinter ClawHub skill page](https://clawhub.ai/yofine/skills/blueprinter)
- [Google Fonts stylesheet used by the HTML template](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with HTML and CSS code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs flat blueprint-style diagram markup and styling guidance; no hidden execution or privileged behavior was identified in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
