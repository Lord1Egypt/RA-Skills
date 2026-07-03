## Description: <br>
Routes A-share market, sector, stock, financial-report, news, and capital-flow requests to specialized daxiapi skills or CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill as a unified entry point for A-share market data requests, including market review, sector analysis, stock screening, financial reports, news, and capital-flow queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DAXIAPI tokens could be exposed through shared chats, screenshots, logs, or pasted command examples. <br>
Mitigation: Keep tokens private, use placeholders in examples, and avoid sharing real token values outside trusted local configuration. <br>
Risk: Stock-selection, timing, valuation, and fixed-investment outputs could be mistaken for personalized investment advice. <br>
Mitigation: Present outputs as informational market analysis only and avoid treating them as instructions to buy, sell, or hold securities. <br>
Risk: The skill depends on daxiapi-cli and referenced market-data APIs. <br>
Mitigation: Confirm the publisher, CLI package, and API service are trusted before installation or use. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [Field Descriptions](references/field-descriptions.md) <br>
- [Daxiapi Website](https://daxiapi.com) <br>
- [Daxiapi API Base URL](https://daxiapi.com/coze) <br>
- [ClawHub Skill Page](https://clawhub.ai/ksky521/skills/daxiapi) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route to specialized analysis skills or provide daxiapi CLI commands; outputs should be treated as informational market analysis.] <br>

## Skill Version(s): <br>
3.0.8 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
