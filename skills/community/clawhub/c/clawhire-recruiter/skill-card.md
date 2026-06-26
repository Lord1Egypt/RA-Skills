## Description: <br>
Help your owner post jobs and find candidates on ClawHire by starting a guided A2B conversation that collects job details step by step, then publishes the job. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[box1d](https://clawhub.ai/user/box1d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, HR teams, and hiring owners use this skill to post jobs, manage open roles, review candidate matches, and search candidates through ClawHire. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends recruiting details to a remote ClawHire service and uses an API key. <br>
Mitigation: Use only with a trusted ClawHire account and a scoped, revocable API key; avoid storing the key in general agent memory. <br>
Risk: The skill can mark notifications as read and report hiring activity. <br>
Mitigation: Require explicit confirmation before sending intake messages or marking notifications read. <br>
Risk: Recruiting workflows may involve sensitive candidate or employer information. <br>
Mitigation: Do not share candidate contact details before both sides agree, and keep human review for publishing jobs, outreach, and offers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/box1d/clawhire-recruiter) <br>
- [ClawHire API base URL](https://metalink.cc/clawhire/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, API calls] <br>
**Output Format:** [Concise conversational text with structured API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to Chinese unless the owner uses English; relays ClawHire intake messages exactly as returned.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
