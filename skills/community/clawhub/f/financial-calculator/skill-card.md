## Description: <br>
Advanced financial calculator with future value tables, present value, discount calculations, markup pricing, and compound interest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarigha](https://clawhub.ai/user/Tarigha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and business operators use this skill to calculate investment growth, present value, discounts, markup pricing, compound interest, and comparison tables through a CLI or local web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The web UI starts a local Flask server for financial calculator inputs. <br>
Mitigation: Run it on a trusted network, prefer localhost binding, and avoid entering highly sensitive financial details. <br>
Risk: The launcher can create a virtual environment and install Flask automatically. <br>
Mitigation: Review the setup before running and use trusted package sources or pinned dependencies where required. <br>
Risk: The web UI loads Chart.js from a CDN. <br>
Mitigation: Use environments where third-party CDN loading is acceptable, or vendor and pin the chart dependency before deployment. <br>


## Reference(s): <br>
- [Financial Formulas Reference](references/formulas.md) <br>
- [ClawHub skill page](https://clawhub.ai/Tarigha/financial-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, Python examples, tabular calculation results, JSON API responses, and local web UI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces financial calculations, comparison tables, and charts; not financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
