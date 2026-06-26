## Description: <br>
Query DataFast website analytics and visitor data via the DataFast API for metrics, time series, realtime stats, breakdowns, visitor details, and goal/payment management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bennyqp](https://clawhub.ai/user/bennyqp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query DataFast analytics, inspect visitor and realtime metrics, and manage goals or payments through the DataFast API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a DataFast API key stored locally and sent to DataFast over HTTPS for authenticated requests. <br>
Mitigation: Protect the key file, avoid pasting the key into prompts, and prefer least-privilege credentials if DataFast supports them. <br>
Risk: The skill can create or delete goals and payments through POST and DELETE requests. <br>
Mitigation: Require a clear preflight summary, exact filters or time range, and explicit user confirmation before any destructive action. <br>


## Reference(s): <br>
- [DataFast homepage](https://datafa.st) <br>
- [ClawHub skill page](https://clawhub.ai/bennyqp/datafast-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with tables and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pagination details when available and requires preflight summaries before destructive requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
