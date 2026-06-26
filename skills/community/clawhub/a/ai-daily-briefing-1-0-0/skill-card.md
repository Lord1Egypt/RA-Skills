## Description: <br>
Start every day focused with a morning briefing that summarizes overdue tasks, today's priorities, calendar overview, and context from recent meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tigertamvip](https://clawhub.ai/user/tigertamvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and productivity-focused agent users use this skill to turn local task lists, meeting notes, memory files, and calendar context into a concise daily or weekly briefing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefings may expose private work context from local task lists, meeting notes, memory files, user files, and calendar entries. <br>
Mitigation: Install only in sessions where the agent is allowed to read and summarize that productivity context, and avoid shared sessions unless private context may appear in the response. <br>
Risk: The briefing can be incomplete or misleading when source files or calendar data are missing, stale, or inconsistent. <br>
Mitigation: Review the generated priorities before acting on them and keep task, meeting, memory, and calendar sources current. <br>


## Reference(s): <br>
- [AI Daily Briefing on ClawHub](https://clawhub.ai/tigertamvip/ai-daily-briefing-1-0-0) <br>
- [Creator homepage](https://jeffjhunter.com) <br>
- [Quick Start](examples/quick-start.md) <br>
- [Example Output](examples/output-example.md) <br>
- [Briefing Preferences Template](assets/PREFERENCES-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown daily briefing with ordered sections, task lists, calendar items, and a focus statement] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes available local productivity context; no code, shell commands, or configuration files are produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
