## Description: <br>
Real-time crypto risk intelligence before and as market stress develops, with Flare for 15-minute precursor detection and Core for 60-minute market context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bilalmotiwala](https://clawhub.ai/user/bilalmotiwala) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch current crypto market-risk summaries and combine immediate Flare alerts with broader Core context. Results should be treated as informational risk intelligence, not automatic trading or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an external BlackSwan service for crypto market-risk information. <br>
Mitigation: Install it only when external service access is acceptable in the agent environment. <br>
Risk: Returned risk assessments may be mistaken for trading or financial advice. <br>
Mitigation: Treat outputs as informational context and require human review before financial decisions. <br>


## Reference(s): <br>
- [BlackClaw ClawHub listing](https://clawhub.ai/bilalmotiwala/blackswan) <br>
- [BlackSwan service](https://mcp.blackswan.wtf) <br>
- [Flare API endpoint](https://mcp.blackswan.wtf/api/flare) <br>
- [Core API endpoint](https://mcp.blackswan.wtf/api/core) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and summarized JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and contacts the external BlackSwan service for latest public risk summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
