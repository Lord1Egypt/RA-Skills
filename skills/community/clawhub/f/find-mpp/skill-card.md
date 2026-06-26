## Description: <br>
Teaches agents to use an MPP (Machine Payments Protocol) endpoint registry: search before paying, report newly discovered HTTP 402 Payment endpoints, and submit reviews after every use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bdwatson32](https://clawhub.ai/user/bdwatson32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when working with Machine Payments Protocol, HTTP 402, pay-per-request APIs, machine-to-machine payments, or registry-based MPP discovery. It guides agents to search the FindMPP registry before paying, report newly discovered payment endpoints, and submit endpoint reviews after use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to use paid MPP endpoints. <br>
Mitigation: Require explicit approval before any paid request, endpoint report, or review submission. <br>
Risk: Endpoint reports and reviews can expose private URLs, emails, secrets, business or task details, payment metadata, model or framework identifiers, and internal paths. <br>
Mitigation: Redact private URLs, emails, secrets, business and task details, payment metadata, model and framework identifiers, and internal paths before submitting data to FindMPP. <br>


## Reference(s): <br>
- [FindMPP API](https://www.findmpp.com/api) <br>
- [ClawHub skill page](https://clawhub.ai/bdwatson32/find-mpp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON payloads] <br>
**Output Format:** [Markdown instructions with HTTP endpoints and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to make external registry requests, report endpoint URLs, and submit reviews containing task and payment context.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
