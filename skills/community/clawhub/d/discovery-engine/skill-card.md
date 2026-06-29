## Description: <br>
Discovery helps agents use Disco to find statistically validated feature interactions, subgroup effects, and conditional relationships in tabular data, returning structured patterns with effect sizes, citations, p-values, and novelty scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessicarumbelow](https://clawhub.ai/user/jessicarumbelow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to run Disco analyses on tabular datasets, inspect columns, choose a target, exclude leakage-prone fields, and retrieve validated patterns and report links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Datasets are uploaded to Disco's external service. <br>
Mitigation: Use the skill only with data that is approved for external processing, and avoid uploading confidential, regulated, proprietary, or personal data unless the deployment has explicit approval. <br>
Risk: Public runs publish data and results. <br>
Mitigation: Before starting any sensitive analysis, explicitly select private visibility and confirm that the run is not public. <br>
Risk: The skill exposes payment, credit purchase, and subscription actions through the agent. <br>
Mitigation: Require human review and confirmation of the exact charge, plan, or payment-method change before allowing the agent to proceed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jessicarumbelow/skills/discovery-engine) <br>
- [Disco homepage](https://disco.leap-labs.com) <br>
- [Disco MCP server](https://disco.leap-labs.com/mcp) <br>
- [Python SDK documentation](docs/python-sdk.md) <br>
- [OpenAPI specification](docs/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration, Python examples, shell commands, and structured analysis summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links, pattern descriptions, p-values, effect sizes, citations, novelty labels, and run status updates from Disco.] <br>

## Skill Version(s): <br>
0.2.141 (source: ClawHub release metadata; artifact package metadata reports 0.2.140) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
