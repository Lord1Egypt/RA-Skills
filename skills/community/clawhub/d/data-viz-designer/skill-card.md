## Description: <br>
A data visualization designer that transforms complex data into clear charts and visualizations through data exploration, chart selection, layout design, detail tuning, and optional interaction design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users use this skill to explore datasets, choose appropriate chart types, and generate browser-ready visualization code or requested SVG/PNG chart outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive data may be exposed if users paste private datasets into the agent or embed them in generated chart code. <br>
Mitigation: Avoid using sensitive datasets unless that use is approved, and redact or aggregate data before generating visualization code. <br>
Risk: Generated HTML or JavaScript may be unsafe to run without review when source data or requested behavior comes from an untrusted source. <br>
Mitigation: Review generated HTML/JavaScript before executing it, especially when using untrusted inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/data-viz-designer) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Guidance] <br>
**Output Format:** [HTML/CSS/JavaScript code, or SVG/PNG image output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Complete browser-ready chart code with embedded data, configuration, and rendering logic; no extra explanatory text unless requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
