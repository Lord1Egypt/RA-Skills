## Description: <br>
Build deterministic, verifiable data visualizations with D3.js from local data files as standalone HTML/SVG and optional PNG outputs without external network dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate reproducible D3 charts, plots, axes, legends, tooltips, and data-driven SVG or HTML outputs from local CSV, TSV, or JSON data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted data rendered into HTML tooltip content could expose users to unsafe markup in generated visualizations. <br>
Mitigation: Sanitize or escape data values before inserting them into tooltip HTML, especially when using sensitive or untrusted datasets. <br>
Risk: The skill text and server evidence differ on the intended D3 version, which can affect reproducibility. <br>
Mitigation: Confirm and pin the D3 version for each generated project before distributing or comparing outputs. <br>
Risk: Capability tags for crypto and purchases are present in metadata but not supported by the described artifact behavior. <br>
Mitigation: Treat those tags as misleading release metadata and evaluate the skill based on the local D3 chart generation behavior described in the artifact and security evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/data-to-d3-d3-visualization) <br>
- [Publisher profile](https://clawhub.ai/user/wu-uk) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with D3.js, HTML, SVG, JavaScript, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Usually produces deterministic files such as dist/chart.html, dist/chart.svg, and optionally dist/chart.png.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
