## Description: <br>
Gate platform activity and campaign hub skill that helps users find trading competitions, airdrops, campaign recommendations, and their enrolled activities through read-only Gate activity queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a configured Gate MCP session use this skill to retrieve Gate campaign recommendations, filter activity types, search activities by name or scenario, and open their enrolled-activities entry without placing orders or changing account state. <br>

### Deployment Geography for Use: <br>
Global, subject to Gate activity availability and regional eligibility. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Gate API credentials for read-only activity lookups. <br>
Mitigation: Use credentials with the minimum Activity:Read permission and keep secrets in local MCP configuration rather than pasting them into chat. <br>
Risk: Generic activity requests may route unintentionally to this Gate-specific skill. <br>
Mitigation: Use explicit prompts such as "my Gate activities" or "Gate trading competitions" when requesting Gate activity-center results. <br>
Risk: Campaign availability, eligibility, and details may change or vary by region. <br>
Mitigation: Verify campaign details in Gate before acting and do not treat activity listings as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gate-exchange-activitycenter-staging) <br>
- [Gate skills homepage](https://github.com/gate/gate-skills) <br>
- [Gate API key management](https://www.gate.com/myaccount/profile/api-key/manage) <br>
- [Gate Activity Center Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate ActivityCenter MCP Specification](references/mcp.md) <br>
- [Scenarios and Prompt Examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown activity cards, tables, links, and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gate activity results; activity list responses are limited to up to three activities per request and require local Gate MCP credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; bundled skill frontmatter: 2026.4.3-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
