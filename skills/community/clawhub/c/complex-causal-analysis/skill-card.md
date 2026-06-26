## Description: <br>
Generates interactive D3.js Sankey-style causal network diagrams that show hierarchical cause-effect relationships with evidence, directional links, and adjustable nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmqnk](https://clawhub.ai/user/zmqnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, educators, and researchers use this skill to turn structured causal factors and relationships into standalone browser visualizations for historical analysis, business root cause analysis, scientific cause-effect chains, and decision mapping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML loads D3.js from an external CDN, which may not fit sensitive, offline, or supply-chain-controlled environments. <br>
Mitigation: Review the generated HTML and use a vetted local copy of D3.js when offline operation or stricter dependency control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmqnk/complex-causal-analysis) <br>
- [D3.js v7](https://d3js.org/d3.v7.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON input structure and standalone HTML visualization code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML loads D3.js v7 from a CDN unless the user reviews or replaces it with a local copy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
