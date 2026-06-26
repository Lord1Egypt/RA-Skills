## Description: <br>
Find things to do and places to eat in any city, including restaurants, bars, concerts, comedy, museums, and live events, by natural-language search, with optional ticket booking and restaurant reservations through Outgoing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[outgoing](https://clawhub.ai/user/outgoing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover real-world activities, restaurants, events, and travel ideas in a city, then optionally create ticket purchases or dining reservations after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends activity, dining, travel, work-meeting, location, and preference details to Outgoing. <br>
Mitigation: Install and use it only when that data sharing is acceptable for the user and organization. <br>
Risk: Ticket purchases and restaurant reservations can create real commitments or charges. <br>
Mitigation: Use dry-run testing first and require clear final user confirmation before submitting any real payment token or booking request. <br>
Risk: Search results may include availability, price, booking, pet-policy, or accessibility details that can change outside the agent. <br>
Mitigation: Report only values returned by the Outgoing API and prompt users to confirm important venue-specific details before acting. <br>


## Reference(s): <br>
- [Outgoing developer documentation](https://www.outgoing.world/developers) <br>
- [Outgoing API reference](https://www.outgoing.world/llms.txt) <br>
- [Outgoing full API reference](https://www.outgoing.world/llms-full.txt) <br>
- [Outgoing homepage](https://outgoing.world) <br>
- [ClawHub skill release page](https://clawhub.ai/outgoing/activity-discovery-and-booking) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Outgoing API responses as the source of truth for venues, events, prices, availability, booking status, and reservation status.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
