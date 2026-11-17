## Description: <br>
Api Gateway Free helps agents route read-only GET requests through Maton's hosted API gateway to connected services such as Slack, Gmail, and Stripe, with basic connection and authentication checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation teams use this skill to check Maton gateway authentication, list configured service connections, and run read-only queries against connected third-party services from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary flags broader local capabilities than the narrow read-only gateway task requires. <br>
Mitigation: Install only when command execution and possible file-write authority are acceptable, and review proposed commands before execution. <br>
Risk: Broad activation language could cause the skill to handle data or tasks outside API gateway lookup work. <br>
Mitigation: Use the skill only for explicit Maton API gateway, connection status, authentication, and read-only third-party account queries. <br>
Risk: Connected third-party services and API keys may expose sensitive account data. <br>
Mitigation: Use read-only service scopes, avoid sending sensitive data unless required, and keep credentials in environment variables without logging or echoing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/api-gateway-free) <br>
- [Maton hosted API gateway](https://api.maton.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only GET/list operations; write actions and trigger management are excluded from the free tier.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
