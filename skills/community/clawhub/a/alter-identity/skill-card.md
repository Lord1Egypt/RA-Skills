## Description: <br>
ALTER Identity connects agents to a hosted MCP service for consent-gated human identity verification, psychometric trait queries, matching, and identity earnings workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxchop](https://clawhub.ai/user/maxchop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use ALTER Identity to configure agents for ALTER's hosted MCP identity service, including free identity lookup tools and optional paid x402-backed trait and matching queries. Agents that handle human data must follow the documented consent and privacy flow before submitting resumes, profiles, social links, or other personal context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may handle resumes, profiles, social links, or other human data through ALTER's hosted service. <br>
Mitigation: Obtain explicit human consent before submission, present ALTER's privacy notice, and do not treat server-side raw-text deletion or PII-redaction claims as protections enforced by this skill. <br>
Risk: Premium tools and an optional Pro API key can introduce paid-query and credential exposure. <br>
Mitigation: Protect the Pro API key, use client-side spending and tool-use controls, and confirm operators understand x402 pricing before enabling paid queries. <br>
Risk: Write-side identity submission workflows described in the artifact are not live on the public MCP server. <br>
Mitigation: Avoid workflows that depend on pending write-side tools until ALTER documents that the per-peer consent architecture is available. <br>


## Reference(s): <br>
- [ClawHub ALTER Identity Listing](https://clawhub.ai/maxchop/alter-identity) <br>
- [ALTER Website](https://truealter.com) <br>
- [ALTER Privacy Notice](https://truealter.com/privacy) <br>
- [ALTER MCP Server](https://mcp.truealter.com/api/v1/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown documentation with MCP configuration JSON and hosted tool-use guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connects agents to a hosted MCP service; an optional ALTER Pro API key raises limits and enables paid-query workflows.] <br>

## Skill Version(s): <br>
0.3.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
