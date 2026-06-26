## Description: <br>
Runs or configures Aicoo's heartbeat loop so an agent can check workspace signals, summarize findings, inspect past runs, and manage heartbeat instructions or policy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aicoo users and their agents use this skill to trigger or configure periodic heartbeat checks across connected workspace data, then receive concise status summaries and run history. It is also used to view or edit HEARTBEAT.md instructions and choose the heartbeat policy tier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heartbeat runs can access sensitive workspace data through connected email, calendar, todo, notes, and memory context. <br>
Mitigation: Use only if you trust Aicoo with the connected workspace data and API key, and prefer the least-privileged credential available. <br>
Risk: The read-only MESSAGES tier is documented inconsistently with write-capable tools such as todo, note, and memory writes. <br>
Mitigation: Keep the default MESSAGES tier unless you are comfortable with autonomous state changes, and review HEARTBEAT.md before running. <br>
Risk: External cron or loop scheduling can repeatedly trigger autonomous checks. <br>
Mitigation: Avoid or tightly limit external scheduling until write permissions and tier behavior are clearly documented, and monitor past heartbeat runs for unexpected activity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xisen-w/aicoo-heartbeat) <br>
- [Aicoo API base](https://www.aicoo.io/api/v1) <br>
- [Heartbeat run endpoint](https://www.aicoo.io/api/v1/heartbeat/run) <br>
- [Heartbeat status endpoint](https://www.aicoo.io/api/v1/heartbeat/status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AICOO_API_KEY or PULSE_API_KEY; heartbeat instructions are maintained as HEARTBEAT.md.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
