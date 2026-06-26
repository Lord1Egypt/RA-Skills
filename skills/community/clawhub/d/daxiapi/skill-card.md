## Description: <br>
Routes A-share market, sector, stock, financial report, and news-analysis requests to the appropriate daxiapi or xiapi analysis skill and provides fallback CLI commands when no specialized skill matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill as a routing layer for A-share market workflows, including market review, sector analysis, stock screening, financial and ROE analysis, news or announcement review, and CLI-based data lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial market outputs or routed analyses could be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational support, verify data independently, and apply human judgment before making investment decisions. <br>
Risk: The daxiapi CLI requires an API token for authenticated data access. <br>
Mitigation: Use the documented configuration flow, avoid sharing tokens in chat, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/daxiapi) <br>
- [Publisher profile](https://clawhub.ai/user/ksky521) <br>
- [daxiapi product site](https://daxiapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route the user to another installed skill or provide daxiapi CLI commands that require a configured API token.] <br>

## Skill Version(s): <br>
3.0.7 (source: target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
