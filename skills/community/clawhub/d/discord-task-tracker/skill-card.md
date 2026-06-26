## Description: <br>
Track tasks in Discord using natural language commands to add, list, complete, and delete tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Discord users and teams use this skill to manage lightweight task lists from chat commands. It supports adding, listing, completing, and deleting tasks while storing task text locally in the skill directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text is stored locally in tasks.json within the skill directory. <br>
Mitigation: Install only when local storage of task text in the skill directory is acceptable. <br>
Risk: Natural language triggers in a busy Discord channel could accidentally create, complete, or delete tasks. <br>
Mitigation: Use explicit prefixes or slash commands when connecting the skill to Discord. <br>
Risk: Completed and deleted tasks are removed from the list, and task IDs may shift after changes. <br>
Mitigation: List tasks before completing or deleting an item to confirm the current task number. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/discord-task-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown/plain text command responses plus JSON task storage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates tasks.json in the skill directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
