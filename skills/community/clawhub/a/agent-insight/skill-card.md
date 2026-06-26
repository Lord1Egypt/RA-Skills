## Description: <br>
Collects customer-facing agent observations about pain points, service improvements, revenue opportunities, churn risk, and field insights, then writes a consolidated Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and customer-success teams use this skill to periodically ask deployed agents for customer insight and turn the responses into a consolidated retention and opportunity report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and persist customer-sensitive operational insights without enough privacy controls. <br>
Mitigation: Run it only in authorized workspaces, use private or access-controlled collection channels, avoid secrets and personal data, and summarize responses instead of storing raw conversation details. <br>
Risk: Broadly sharing insight prompts may expose customer context to unintended recipients. <br>
Mitigation: Confirm the channel, recipients, and retention rules before each run, and define deletion rules for stored reports. <br>


## Reference(s): <br>
- [Agent Insight on ClawHub](https://clawhub.ai/mupengi-bot/agent-insight) <br>
- [Sample Agent Insight Report](references/sample-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report and concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the consolidated report to memory/insights/YYYY-MM-DD-agent-insight.md when run in an authorized workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
