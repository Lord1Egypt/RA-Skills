## Description: <br>
Helps agents keep working proactively from a task queue instead of waiting for prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up task queues, proactive heartbeats, and handoff notes so agents can continue queued work between human prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled work can update files or accounts beyond the user's intent. <br>
Mitigation: Define approved task sources, allowed directories and accounts, forbidden actions, logging, token and spend limits, review gates for high-impact work, and a clear pause or removal process before enabling cron or heartbeat automation. <br>
Risk: Team spawning and external status posts can disclose sensitive work or trigger unwanted coordination. <br>
Mitigation: Limit channel permissions, approve posting destinations, and require human review for high-impact handoffs or external updates. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lean-zhouchao/agent-autonomy-kit-zc) <br>
- [README](README.md) <br>
- [Proactive Heartbeat template](templates/HEARTBEAT.md) <br>
- [Task Queue template](templates/QUEUE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and JSON-style configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes queue and heartbeat templates; no direct API calls or credential variables were detected in the release evidence.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
