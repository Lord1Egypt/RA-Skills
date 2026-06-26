## Description: <br>
Auto Reflection automates recurring learning reflection by generating reflection reports, updating capability assessments, adjusting learning plans, and optimizing knowledge graph data every five learning rounds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyblhl](https://clawhub.ai/user/wyblhl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to automate periodic self-reflection over local learning records, capability assessments, and knowledge graph data. It produces summaries, improvement suggestions, and next-step learning plans after learning rounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes reflection reports, logs, HEARTBEAT.md, capabilities.json, and knowledge-graph.json in the local OpenClaw workspace. <br>
Mitigation: Review or back up those files before installation and require confirmation before writes when using it in a shared or important workspace. <br>
Risk: Automatic reflection can persistently update local learning state every five learning rounds. <br>
Mitigation: Narrow triggers, disable automatic execution, or run the script manually when a reflection pass is intended. <br>


## Reference(s): <br>
- [Auto Reflection on ClawHub](https://clawhub.ai/wyblhl/auto-reflection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON reflection reports, Markdown HEARTBEAT.md updates, and console or log text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a local OpenClaw workspace using fixed Windows paths unless the script is modified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
