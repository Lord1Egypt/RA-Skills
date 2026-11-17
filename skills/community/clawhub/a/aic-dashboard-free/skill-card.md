## Description: <br>
Aic Dashboard Free provides a local, read-only dashboard for monitoring recent inbox entries and browser session status with token-protected localhost access and periodic refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using AI Commander use this skill to inspect recent inbound mail and browser-session state from a local monitoring dashboard during development or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard reads local inbox and browser-session data, which may expose sensitive operational information if access is broadened or the token leaks. <br>
Mitigation: Keep the service bound to localhost, treat the dashboard URL token as sensitive, and avoid exposing it beyond the local machine. <br>
Risk: The inspected artifact describes executing a Node dashboard but does not include the referenced implementation file. <br>
Mitigation: Review the actual Node script before running it and install only when a local inbox and session dashboard is specifically needed. <br>
Risk: Security evidence flags overly broad activation guidance and weakly scoped authority. <br>
Mitigation: Limit use to the documented local monitoring workflow and review requested file access before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aic-dashboard-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a local read-only dashboard that reads ./data/inbox.jsonl and ./data/session.json and refreshes periodically.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
