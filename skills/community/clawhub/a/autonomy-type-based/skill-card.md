## Description: <br>
Type-based autonomous task queue system. Categorizes tasks by type (research, writing, analysis, maintenance) and lets autonomy work only on value-add tasks while cron handles maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciusrockwing](https://clawhub.ai/user/luciusrockwing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to structure an agent's local autonomous work around research, writing, and analysis tasks while leaving maintenance, backup, and security work to separate scheduled processes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates maintenance, backup, and security tasks to separate scheduled processes, so those tasks may be missed if cron or an equivalent process is not actually configured. <br>
Mitigation: Before enabling the workflow, confirm a separate process handles skipped maintenance, backup, and security tasks. <br>
Risk: The artifact's goal examples are generic and may steer autonomous work toward objectives that do not match the user's intent. <br>
Mitigation: Edit the goal text and task labels to match the user's own objectives before allowing autonomous queue work. <br>
Risk: Autonomous queue updates can change task, memory, goal, and learning files over time. <br>
Mitigation: Keep tasks, memory, GOALS.md, and .learnings/ under version control or regular human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luciusrockwing/autonomy-type-based) <br>
- [README.md](README.md) <br>
- [Queue template](templates/QUEUE.md) <br>
- [Heartbeat template](templates/HEARTBEAT.md) <br>
- [Checkpoint formats](references/checkpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown templates and procedural instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses @type labels, priority tags, queue sections, heartbeat checks, and completion logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
