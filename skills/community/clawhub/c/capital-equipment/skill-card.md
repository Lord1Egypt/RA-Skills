## Description: <br>
Search, book, and manage scientific research equipment across facilities, track usage, submit service requests, and find collaborators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cesco345](https://clawhub.ai/user/cesco345) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, lab managers, and research operations teams use this skill to find suitable shared instruments, check availability, manage bookings, request services, monitor equipment opportunities, and coordinate with collaborators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a remote equipment service, so user queries and equipment activity may leave the local agent environment. <br>
Mitigation: Confirm the service's retention, access, and deletion controls before connecting it or sending sensitive research or procurement details. <br>
Risk: The skill can save research profile details such as institution, interests, watched equipment, and notification channel in persistent memory. <br>
Mitigation: Store only necessary preferences and avoid saving confidential research plans, procurement strategy, or sensitive institutional information. <br>


## Reference(s): <br>
- [Capital Equipment Network (CapNetEq) on ClawHub](https://clawhub.ai/cesco345/capital-equipment) <br>
- [Capital Equipment MCP endpoint](https://us-central1-capital-equipment-dev.cloudfunctions.net/mcpServer/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown] <br>
**Output Format:** [Markdown with JSON and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a remote MCP service and persistent memory for saved research preferences, watched equipment, and notification settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
