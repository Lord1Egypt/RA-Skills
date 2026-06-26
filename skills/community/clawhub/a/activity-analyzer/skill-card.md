## Description: <br>
Use ActivityWatch to analyze user's computer activity (Requires Node.js). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qew21](https://clawhub.ai/user/qew21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and productivity-focused users use this skill to query local ActivityWatch activity for a recent time window, summarize time distribution, identify patterns, and receive actionable productivity advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ActivityWatch app names and window titles may expose sensitive document names, URLs, email subjects, or other private activity details to the AI model. <br>
Mitigation: Review output before sharing, redact or aggregate window titles, remove raw result printing when possible, and collect only the time range needed for the analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qew21/activity-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown analysis with plain-text command output from a local Node.js script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The command queries the last 24 hours by default, prints up to 50 activity records longer than one minute, and may include raw app names and window titles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
