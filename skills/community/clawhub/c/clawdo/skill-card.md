## Description: <br>
Todo list and task management for AI agents. Add, track, and complete tasks with autonomy levels — agents propose work, humans approve. Works in heartbeats, cron, and conversations. Persistent SQLite CLI with structured JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LePetitPince](https://clawhub.ai/user/LePetitPince) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a persistent task queue that agents can inspect, propose to, and execute from conversations, heartbeat loops, cron jobs, or sub-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended heartbeat or cron use could cause agents to act on tasks without enough human oversight. <br>
Mitigation: Limit unattended use to clearly scoped, pre-approved, low-risk work and require human review before tasks involving accounts, money, public content, production systems, credentials, or private data. <br>
Risk: The skill depends on a globally installed npm CLI that maintains a persistent task queue. <br>
Mitigation: Install only in environments where the global clawdo CLI and its persistent queue are acceptable, and keep CLI usage visible to operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LePetitPince/clawdo) <br>
- [npm package](https://www.npmjs.com/package/clawdo) <br>
- [Release notes](https://github.com/LePetitPince/clawdo/releases/tag/v1.1.4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing guidance expects the external clawdo CLI binary and structured JSON CLI output.] <br>

## Skill Version(s): <br>
1.1.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
