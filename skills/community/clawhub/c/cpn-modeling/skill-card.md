## Description:

This skill helps agents turn natural-language business process descriptions into Colored Petri Net models, including structured JSON, CPN Tools XML, and an animated HTML visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theosunny](https://clawhub.ai/user/theosunny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and process designers use this skill to model workflows with concurrency, synchronization, dependencies, and resource contention. It supports guided elicitation for vague business descriptions and can produce machine-readable CPN artifacts plus browser-based visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML visualizations may execute injected script if untrusted process descriptions are embedded without safe serialization.

Mitigation: Review generated HTML before opening it for untrusted inputs, and ensure the CPN data is safely serialized so closing script tags and executable markup cannot be injected.

## Reference(s):

- [CPN Modeling Skill Page](https://clawhub.ai/theosunny/skills/cpn-modeling)
- [CPN JSON Schema Reference](artifact/references/json-schema.md)
- [CPN Modeling Guide](artifact/references/modeling-guide.md)
- [CPN XML Template Reference](artifact/references/cpn-xml-template.md)
- [HTML Visualization Template Reference](artifact/references/html-viz-template.md)
- [Restaurant Modeling Example](artifact/references/example-restaurant.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance]

**Output Format:** [Markdown containing JSON, CPN Tools XML, generated HTML file guidance, and shell commands for opening the visualization]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated HTML visualization is written to /tmp/<project_id>.html rather than printed into the conversation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
