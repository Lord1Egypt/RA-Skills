## Description: <br>
Automate Calendly scheduling, event management, invitee tracking, availability checks, and organization administration via Rube MCP (Composio). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sohamganatra](https://clawhub.ai/user/sohamganatra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through Calendly scheduling workflows, including listing events, checking availability, creating scheduling links, managing invitees, canceling events, and administering organization invitations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide event cancellation and organization administration actions that may affect other people's schedules or account access. <br>
Mitigation: Confirm the target event, invitee, organization, or user with the requester before executing high-impact Calendly actions. <br>
Risk: The skill depends on an external Rube MCP connection and Calendly OAuth permissions. <br>
Mitigation: Install only when the Rube MCP connection is trusted and grant only the Calendly permissions needed for the intended workflows. <br>


## Reference(s): <br>
- [Rube MCP endpoint](https://rube.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with tool sequences, parameters, and cautions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide an agent to use Rube MCP Calendly tools and to confirm high-impact actions before execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
