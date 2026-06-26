## Description: <br>
DataHub unifies financial data retrieval across market quotes, financial statements, announcements, macroeconomic data, research reports, and investor-relations sources with publish-subscribe routing, caching, and quick access helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and financial research teams use this skill to configure and call a unified DataHub layer for market, company, macroeconomic, announcement, research, and investor-relations data. It supports batch retrieval, multi-source comparison, natural-language query helpers, and research workflow integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses API keys and cookies for some financial data providers. <br>
Mitigation: Store provider credentials in approved secret-management or local environment configuration, avoid committing them, and rotate them if exposed. <br>
Risk: Financial research queries and identifiers may be sent to external data providers. <br>
Mitigation: Use approved providers for confidential work, prefer local or explicitly selected sources when privacy matters, and review provider terms before use. <br>


## Reference(s): <br>
- [DataHub Unified Data Layer on ClawHub](https://clawhub.ai/cgxxxxxxxxxxxx/datahub-unified) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, shell commands] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and examples for configuring DataHub paths, API credentials, subscriptions, caching, retries, monitoring, and financial data retrieval workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
