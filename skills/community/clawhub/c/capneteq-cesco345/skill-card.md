## Description: <br>
Search, book, and manage scientific research equipment at 200+ institutions with real-time availability, service requests, and collaborator discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cesco345](https://clawhub.ai/user/cesco345) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers and research operations staff use this skill to discover, reserve, and manage shared scientific instruments, submit service requests, and find collaborators through the Capital Equipment platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth authorization can allow the assistant to make real bookings or submit service requests on the user's behalf. <br>
Mitigation: Require explicit confirmation of facility, instrument, time, price, institution, and cancellation terms before submitting a booking or request. <br>
Risk: Optional proactive automations may monitor saved searches, bookings, marketplace listings, calendars, or public researcher profiles. <br>
Mitigation: Keep automations disabled unless the user explicitly enables the specific monitoring workflow they want. <br>
Risk: The release has no license identifier in the server evidence. <br>
Mitigation: Confirm terms of use with the publisher or platform before redistribution or commercial deployment. <br>


## Reference(s): <br>
- [Capital Equipment ClawHub listing](https://clawhub.ai/cesco345/capneteq-cesco345) <br>
- [Capital Equipment MCP server](https://capneteq.com/mcpServer/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initiate OAuth-authorized bookings, service requests, availability checks, and optional user-enabled monitoring workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
