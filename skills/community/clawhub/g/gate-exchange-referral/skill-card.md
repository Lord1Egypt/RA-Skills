## Description: <br>
Gate invite-friends and referral campaign skill for referral activity recommendations, rule interpretation, personalized activity selection, and referral FAQ handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to explain Gate referral programs, recommend suitable invite-friends activities, and answer reward timing, eligibility, and referral-link questions. <br>

### Deployment Geography for Use: <br>
Global, subject to Gate regional eligibility and activity rules. <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external mutable runtime-rules file that can change after release. <br>
Mitigation: Review the referenced runtime rules before deployment and re-check them when the skill behavior or security posture is reviewed. <br>
Risk: Gate MCP or API authentication may be requested for account-scoped referral functionality. <br>
Mitigation: Authorize Gate MCP or API credentials only when account-scoped functionality is needed, and use least-privileged credentials. <br>
Risk: The skill can provide referral guidance that may not reflect a user's current region, eligibility, or live reward status. <br>
Mitigation: Use the official Gate referral page for current campaign details, regional requirements, and reward-progress checks. <br>


## Reference(s): <br>
- [Gate Invite Friends page](https://www.gate.com/referral) <br>
- [Gate Exchange Referral Skill on ClawHub](https://clawhub.ai/gate-exchange/gate-exchange-referral) <br>
- [Gate Referral MCP Specification](references/mcp.md) <br>
- [Referral Scenario Reference](references/scenarios.md) <br>
- [Gate runtime rules referenced by the skill](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with structured referral recommendations and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes official referral-page links and redirects unsupported account or reward-progress queries to Gate.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
