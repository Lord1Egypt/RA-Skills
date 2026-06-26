## Description: <br>
Automate Cal.com tasks via Rube MCP (Composio): manage bookings, check availability, configure webhooks, and handle teams. Always search tools first for current schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Cal.com scheduling workflows through Rube MCP, including bookings, availability checks, webhook configuration, team handling, and organization lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account-changing Cal.com actions such as creating bookings, changing teams, and updating or deleting webhooks. <br>
Mitigation: Review booking details, team names, webhook IDs, event triggers, and subscriber URLs before approving changes. <br>
Risk: Webhook configuration can involve sensitive signing secrets and externally reachable subscriber URLs. <br>
Mitigation: Treat webhook secrets as sensitive credentials and use only trusted HTTPS endpoints under your control. <br>
Risk: Cal.com access is brokered through Rube/Composio. <br>
Mitigation: Install only when you trust Rube/Composio and connect the intended Cal.com account. <br>


## Reference(s): <br>
- [Rube MCP server](https://rube.app/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/sohamganatra/cal-com-automation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes tool sequences, required parameters, setup steps, pitfalls, and review guidance for Cal.com actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
