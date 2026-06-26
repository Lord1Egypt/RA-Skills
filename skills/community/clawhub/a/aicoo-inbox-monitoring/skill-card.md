## Description: <br>
Monitors Aicoo inbox activity, new conversations, pending requests, and optional network context so an agent can surface items that need action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to monitor Aicoo conversations and network requests, prioritize new inbound items, and produce concise suggested next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Aicoo API key to read private inbox, request, and optional network-context data. <br>
Mitigation: Install only when this access is intended, use explicit Aicoo monitoring commands, and prefer the least-privileged Aicoo token available. <br>
Risk: Recurring loop, routine, or cron usage can repeatedly poll sensitive inbox data. <br>
Mitigation: Use recurring monitoring only when periodic polling is desired and configure a narrow interval, view, limit, and state file appropriate to the task. <br>


## Reference(s): <br>
- [Aicoo API base URL](https://www.aicoo.io/api/v1) <br>
- [Aicoo conversations endpoint](https://www.aicoo.io/api/v1/conversations?view=all&limit=50) <br>
- [Aicoo network requests endpoint](https://www.aicoo.io/api/v1/network/requests) <br>
- [Aicoo network context endpoint](https://www.aicoo.io/api/v1/os/network) <br>
- [ClawHub skill page](https://clawhub.ai/xisen-w/aicoo-inbox-monitoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON-shaped status fields and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports new message counts, incoming request counts, urgent items, and suggested next actions; returns a single no-activity line when nothing changed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
