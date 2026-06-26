## Description: <br>
A-Share Multi-Dimensional Quantitative Analysis MCP Server - broker research reports, AI news analysis, and stock comprehensive analysis <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Li-Evan](https://clawhub.ai/user/Li-Evan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this hosted MCP server to query A-share broker research reports, AI-analyzed news, and stock analysis reports from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer API keys may be sent over a plain HTTP MCP endpoint. <br>
Mitigation: Use the skill only through a trusted network path, avoid sensitive financial research until HTTPS is available, and ask the publisher for an HTTPS endpoint. <br>
Risk: The artifact includes weak default secrets and database credentials. <br>
Mitigation: Ask the publisher to rotate and remove backend credentials before using the skill with sensitive data. <br>
Risk: Data retention and access scope are not clearly documented. <br>
Mitigation: Confirm retention, access scope, and provider trust before connecting agent workflows or sharing sensitive queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Li-Evan/a-share-multidim-quant-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration] <br>
**Output Format:** [Markdown text returned by MCP tools, plus JSON configuration for setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool responses may include broker research report text, news summaries, sentiment analysis, investment recommendations, risk management notes, and trading decision sections.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata; artifact frontmatter says 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
