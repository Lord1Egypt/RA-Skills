## Description: <br>
Acuity Scheduling API integration with managed OAuth for managing appointments, calendars, clients, and availability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to read and manage Acuity Scheduling appointments, availability, calendars, clients, blocks, forms, and labels through Maton's OAuth-backed API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and OAuth connection that can access scheduling data in the connected Acuity account. <br>
Mitigation: Install only when you trust Maton, keep MATON_API_KEY out of logs and shared files, connect only the intended Acuity account, and revoke or delete the OAuth connection when it is no longer needed. <br>
Risk: Create, update, cancel, and delete operations can change appointments, clients, and availability blocks. <br>
Mitigation: Before approving any write or delete action, verify the exact account, target resource, and intended effect with the user. <br>
Risk: When multiple Acuity accounts are connected, requests may target the wrong account if the connection is not specified. <br>
Mitigation: Use the Maton-Connection header whenever multiple Acuity Scheduling connections exist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/acuity-scheduling) <br>
- [Acuity Scheduling API Quick Start](https://developers.acuityscheduling.com/reference/quick-start) <br>
- [Appointments API](https://developers.acuityscheduling.com/reference/get-appointments) <br>
- [Availability API](https://developers.acuityscheduling.com/reference/get-availability-dates) <br>
- [Calendars API](https://developers.acuityscheduling.com/reference/get-calendars) <br>
- [Clients API](https://developers.acuityscheduling.com/reference/clients) <br>
- [OAuth2 Documentation](https://developers.acuityscheduling.com/docs/oauth2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and an Acuity Scheduling OAuth connection; write and delete operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
