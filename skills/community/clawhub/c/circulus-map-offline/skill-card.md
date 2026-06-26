## Description: <br>
Use when the user wants aviation route maps, ETOPS-aware route analysis, projection comparisons, airport lookup, or SVG map rendering through a local Circulus Map MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and aviation workflow users use this skill to solve routes, compare projections, prepare ETOPS-aware map specifications, look up airports, and render export-ready SVG maps through a local Circulus Map MCP worker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a localhost MCP endpoint, so a misconfigured endpoint could route requests to a service the operator does not control. <br>
Mitigation: Confirm the configured MCP URL points to the intended local Circulus Map worker before using route-solving or rendering tools. <br>
Risk: The local app and worker are separate runtime components outside this skill package. <br>
Mitigation: Review and run the local app and MCP worker in the intended environment before relying on generated route analysis or SVG output. <br>


## Reference(s): <br>
- [Local setup](references/local-setup.md) <br>
- [MapSpecV1 notes](references/mapspec.md) <br>
- [Input understanding guide](references/input-understanding.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, SVG, Shell commands, Configuration] <br>
**Output Format:** [Markdown responses with route guidance, MapSpecV1 JSON, shell commands, configuration notes, and SVG rendering output when the local MCP worker is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an operator-controlled localhost Circulus Map MCP worker for tool execution.] <br>

## Skill Version(s): <br>
1.3.24 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
