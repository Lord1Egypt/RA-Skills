## Description:

A Model Context Protocol (MCP) calculator skill for addition, subtraction, multiplication, division, powers, square roots, and integer factorials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route numeric calculation requests through the XiaoBenYang MCP service and return formatted calculation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a plaintext .env file.

Mitigation: Use a dedicated low-privilege API key, restrict workspace access, and remove or rotate the key after use.

Risk: Calculation inputs are sent to an external XiaoBenYang service.

Mitigation: Do not send sensitive inputs; prefer a local calculator skill for basic arithmetic when remote processing is unnecessary.

Risk: The skill depends on a remote service for results, even for basic arithmetic.

Mitigation: Review outputs before relying on them and have a local fallback for simple calculations or offline use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cainingnk/skills/calculator-kel)
- [XiaoBenYang API Key Site](https://xiaobenyang.com)
- [XiaoBenYang MCP Service Endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text summarizing JSON responses from the remote calculation service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; calculation results depend on remote service availability and response correctness.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
