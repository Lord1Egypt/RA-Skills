## Description: <br>
Retrieve fresh, relevant, and citation-backed web information using neural and keyword search via the Exa API for up-to-date answers and content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this instructional skill to decide when and how to call Exa search, contents, findSimilar, answer, and beta research operations for fresh web retrieval, source evaluation, citation-grounded answers, and cost-aware research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, or retrieved content may expose confidential information to an external Exa service. <br>
Mitigation: Configure EXA_API_KEY only in the tool or MCP layer, avoid confidential queries and private URLs, and strip unnecessary query parameters before retrieval. <br>
Risk: Retrieved web pages can contain misleading content or prompt-injection instructions. <br>
Mitigation: Treat web content as untrusted data, ignore embedded instructions, evaluate source quality, and corroborate material claims before presenting them. <br>
Risk: Repeated broad searches or full-content retrieval can increase API cost. <br>
Mitigation: Use focused queries, conservative result limits, cheaper search types when sufficient, and request summaries or highlights before full text. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/simonpierreboucher02/exa-api-al) <br>
- [Exa API Documentation](https://docs.exa.ai) <br>
- [Exa Endpoints Reference](reference/endpoints.md) <br>
- [Exa Parameters Reference](reference/parameters.md) <br>
- [Exa Safety and Security Reference](reference/safety-and-security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with inline examples, source lists, and API configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Exa-capable tool or HTTP client and an EXA_API_KEY configured outside the skill text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
