## Description: <br>
MiCA compliance evidence and stablecoin risk scoring for regulated tokenized markets, with ES256K-signed responses for explicit stablecoin compliance, MiCA status, and audit evidence workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[feedoracle](https://clawhub.ai/user/feedoracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, compliance teams, and agent developers use this skill when they explicitly need signed evidence for stablecoin MiCA status, issuer due diligence, risk scoring, peg monitoring, reserve data, or audit review workflows. The skill should present signed evidence and supporting identifiers rather than making absolute compliance claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-initiated tools can send question text, agent metadata, decision text, or evidence request IDs to FeedOracle services. <br>
Mitigation: Invoke FeedOracle only for explicit compliance, MiCA, stablecoin, or audit requests; send only the minimum required fields and get explicit consent before audit logging, agent registration, or report generation. <br>
Risk: Signed compliance evidence can be misread as an absolute legal determination. <br>
Mitigation: Call the relevant evidence tool before making status statements, present the signed data and identifiers, and let the user make the final decision. <br>
Risk: Higher-limit API access and signed report generation may require an API key. <br>
Mitigation: Use the no-key free tier when sufficient, avoid exposing API keys, and only request report generation when the user explicitly asks for it. <br>


## Reference(s): <br>
- [FeedOracle Homepage](https://feedoracle.io) <br>
- [FeedOracle API Docs](https://feedoracle.io/docs) <br>
- [FeedOracle MCP Server](https://github.com/feedoracle/feedoracle-mcp) <br>
- [FeedOracle Trust Policy](https://github.com/feedoracle/feedoracle-mcp/blob/main/docs/TRUST_POLICY.md) <br>
- [FeedOracle JWKS](https://feedoracle.io/.well-known/jwks.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/feedoracle/feedoracle-compliance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and references to signed MCP evidence responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite ES256K signature details, pack IDs, and JWKS verification URLs when evidence is returned.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata; artifact frontmatter reports 1.2.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
