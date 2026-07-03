## Description: <br>
Orchestrates Fulcra concierge sub-skills into morning, evening, and day-of routing flows with graceful degradation when dependencies are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keng009](https://clawhub.ai/user/keng009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill as the front door for a Fulcra personal concierge workflow, including morning check-ins and briefings, evening debriefs, weekly meeting cadence insight, and contextual routing to related concierge skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes broad Fulcra and Attio clients capable of reading, writing, and deleting sensitive personal and CRM data. <br>
Mitigation: Install only in a trusted environment, control Fulcra and Attio tokens and related API base environment variables, and require dry-run or explicit confirmation before CRM or annotation mutations. <br>
Risk: The concierge workflow can touch intimate personal context such as feelings, sleep, calendar, and relationships. <br>
Mitigation: Avoid public or group-context use for private details and do not print API tokens or secrets. <br>


## Reference(s): <br>
- [Personal Concierge on ClawHub](https://clawhub.ai/keng009/skills/fulcra-concierge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route requests to other concierge skills and may produce JSON status output when the status script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
