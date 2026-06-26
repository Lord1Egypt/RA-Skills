## Description: <br>
Query equipment status, maintenance schedules, and service history for the farm fleet. Uses integration endpoints with no authentication required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianppetty](https://clawhub.ai/user/brianppetty) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Farm operators, mechanics, and agent developers use this skill to check equipment status, due maintenance, service history, parts information, and equipment issue reports for a farm fleet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write safety-relevant maintenance, hour, and task records through integration endpoints with broad or unclear controls. <br>
Mitigation: Install only after confirming the backend requires authentication and authorization for all write endpoints and keeps auditable records of write actions. <br>
Risk: Maintenance completion or hour logging based on vague or incomplete reports could create inaccurate operational records. <br>
Mitigation: Ask the user before completing maintenance or logging hours, and include the observed source details in the recorded action. <br>
Risk: Critical-mode escalation can create notifications or tasks for safety-related reports without waiting for the reporter to request it. <br>
Mitigation: Define narrow, auditable critical-mode triggers and confirm that automatic notification and task creation policies are acceptable for the farm operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianppetty/farmos-equipment) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Natural language responses with JSON API request bodies when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include follow-up questions, maintenance status summaries, issue intake notes, and task or maintenance-record action proposals.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
