## Description:

Use when the user wants aviation route maps, ETOPS-aware route analysis, projection comparisons, airport lookup, or SVG map rendering through a local Circulus Map MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skylinehk](https://clawhub.ai/user/skylinehk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and aviation workflow operators use this skill to solve local route-map requests, normalize route inputs, build MapSpecV1 payloads, compare projections, evaluate ETOPS scenarios, and render export-ready SVG maps through an operator-controlled localhost MCP worker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes aviation map requests through a localhost MCP endpoint.

Mitigation: Install it only for workflows that intentionally use a local Circulus Map MCP worker, and verify that the configured localhost endpoint is controlled by the operator.

Risk: Malformed or ambiguous airport and route inputs can produce incorrect map requests.

Mitigation: Use the bundled input-understanding guidance to normalize route phrasing, search ambiguous locations before solving, and echo important resolution choices before final SVG rendering.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skylinehk/skills/circulus-map-offline)
- [Local setup](references/local-setup.md)
- [MapSpecV1 notes](references/mapspec.md)
- [Input understanding guide](references/input-understanding.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MapSpec examples, shell commands, MCP tool calls, and SVG rendering outputs when the local worker is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an operator-controlled localhost MCP endpoint; no hosted credentials are required in normal flows.]

## Skill Version(s):

1.3.24 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
