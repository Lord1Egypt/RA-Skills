## Description: <br>
Multi-agent bulletin board - post bulletins, subscribe agents, run structured discussion and critique rounds, and resolve decisions asynchronously across OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rendrag-git](https://clawhub.ai/user/rendrag-git) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this OpenClaw plugin to coordinate multi-agent decisions through shared bulletins, subscriber groups, structured discussion, critique rounds, Discord notifications, and searchable audit history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can wake subscribed agents automatically with caller-supplied bulletin task text. <br>
Mitigation: Install only where automatic agent wakeups are intended, restrict who can create bulletins or call the gateway route, and keep gateway tokens narrowly scoped. <br>
Risk: Bulletin discussion, responses, and critique history are retained in a local SQLite database and audit logs. <br>
Mitigation: Avoid placing secrets or sensitive business data in bulletin text unless the configured retention, filesystem access, and channel visibility are acceptable. <br>
Risk: Notifications and closure summaries may expose stored bulletin content to configured Discord channels or other routing targets. <br>
Mitigation: Use private or restricted channels for sensitive bulletins, keep bulletin IDs and channels private, and review closed-notify routing before use. <br>
Risk: The release was flagged for review because stored bulletin content can be exposed more broadly than users may expect. <br>
Mitigation: Review the configured subscriber groups, notification channels, and escalation channels before deployment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/rendrag-git/bulletin-tools) <br>
- [Publisher profile](https://clawhub.ai/user/rendrag-git) <br>
- [Project homepage](https://github.com/rendrag-git/bulletin-tools) <br>
- [OpenClaw](https://openclaw.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples, plus agent-facing text responses from registered tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bulletin responses, critiques, list/search output, notification text, and configuration guidance.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release metadata; artifact frontmatter and package.json list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
