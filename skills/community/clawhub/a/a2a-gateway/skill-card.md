## Description: <br>
A2a Gateway provides a local agent service bus for registering agent cards, routing work to matching agents, tracking delegated tasks, recording audit events, and checking agent health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage an OpenClaw multi-agent network: register agent capabilities, route user intents to agents, track task lifecycle events, review audit trails, and run health or performance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local audit and task history for the agent bus. <br>
Mitigation: Review what data will be written before use, avoid storing sensitive task content unless needed, and periodically inspect or prune local audit and task records. <br>
Risk: Running setup-cron.sh can add a recurring health-check cron job. <br>
Mitigation: Inspect the cron command first, run the setup only after consent, and verify or remove the entry with crontab if scheduled checks are not wanted. <br>
Risk: pending_spawn.json behavior may enable automatic spawning or dispatch validation. <br>
Mitigation: Review pending_spawn.json before allowing automatic spawning, and keep spawning disabled unless the target agent and task are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/a2a-gateway) <br>
- [Publisher profile](https://clawhub.ai/user/perrykono-debug) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local JSON or JSONL records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local agent registry, routing, task, audit, health, and performance artifacts under the configured workspace.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
