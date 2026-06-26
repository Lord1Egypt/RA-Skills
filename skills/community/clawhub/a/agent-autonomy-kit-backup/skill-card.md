## Description: <br>
Stop waiting for prompts. Keep working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up task queues, proactive heartbeat routines, and handoff notes so an agent can continue meaningful work between human prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables unattended autonomous work and may let agents make broad changes without enough user-control boundaries. <br>
Mitigation: Define an approved task queue, cap runtime and budget, and require human approval for deployments, external posts, account changes, destructive edits, and sensitive data use. <br>
Risk: Cron, memory-writing, queue-editing, team-posting, and multi-agent workflows can amplify mistakes if enabled without review. <br>
Mitigation: Review and scan the skill before deployment, start with limited permissions, and verify the intended source before cloning or installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayakolin/agent-autonomy-kit-backup) <br>
- [Publisher profile](https://clawhub.ai/user/ayakolin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with setup steps, task queue templates, heartbeat templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions and templates; users should review boundaries before enabling unattended work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
