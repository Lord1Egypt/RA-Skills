## Description:

Generates interactive D3.js Sankey-style causal network diagrams that show hierarchical cause-and-effect relationships with evidence, draggable nodes, directional arrows, and color-coded relationship strengths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmqnk](https://clawhub.ai/user/zmqnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to turn causal factors and relationships into interactive browser visualizations for historical analysis, business root cause analysis, scientific cause-effect chains, problem diagnosis, and decision mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can execute unsafe browser JavaScript when graph data comes from an untrusted source.

Mitigation: Review generated HTML before opening it, escape graph labels and descriptions, and validate color and strength values before rendering.

Risk: The generated page may load D3 from a remote script URL.

Mitigation: Bundle D3 locally or pin the remote dependency with integrity checking before controlled or commercial use.

## Reference(s):

- [Complex Causal Analysis on ClawHub](https://clawhub.ai/zmqnk/skills/complex-causal-analysis)
- [D3.js](https://d3js.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Markdown guidance and standalone HTML/CSS/JavaScript output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates browser-viewable D3.js causal network visualizations from supplied node and link data; generated HTML may load D3 from a CDN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
