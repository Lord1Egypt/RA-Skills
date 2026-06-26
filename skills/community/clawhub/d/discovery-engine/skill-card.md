## Description: <br>
Automatically discover novel, statistically validated patterns in tabular data, including feature interactions, subgroup effects, and conditional relationships, with hold-out validation, FDR-corrected p-values, literature checks, effect sizes, citations, and novelty scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessicarumbelow](https://clawhub.ai/user/jessicarumbelow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to run Disco on tabular datasets and surface statistically validated patterns that may not emerge from hypothesis-driven analysis. It helps agents guide uploads, target-column selection, cost estimation, execution, polling, and result interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local, private, proprietary, regulated, or personal datasets to Disco. <br>
Mitigation: Prefer private analysis for sensitive data, confirm the exact file path before local upload, and avoid sending data the user has not explicitly approved for analysis. <br>
Risk: Public analyses can publish results. <br>
Mitigation: Ask the user to choose public or private visibility before submitting a run, and use private analysis when results or source data should not be public. <br>
Risk: The skill can perform paid account and billing actions. <br>
Mitigation: Call cost-estimation tools before private runs and require explicit user approval before attaching payment methods, buying credits, or changing subscriptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessicarumbelow/skills/discovery-engine) <br>
- [Disco homepage](https://disco.leap-labs.com) <br>
- [Disco MCP endpoint](https://disco.leap-labs.com/mcp) <br>
- [Python SDK documentation](docs/python-sdk.md) <br>
- [OpenAPI specification](docs/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, API/tool-call instructions, and structured analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report URLs, pattern descriptions, conditions, effect sizes, p-values, novelty classifications, citations, feature importance, account status, and credit-cost estimates returned by Disco.] <br>

## Skill Version(s): <br>
0.2.139 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
