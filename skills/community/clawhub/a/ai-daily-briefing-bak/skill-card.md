## Description: <br>
Start every day focused. Get a morning briefing with overdue tasks, today's priorities, calendar overview, and context from recent meetings. Works with ai-meeting-notes to-do list. No setup. Just say 'briefing'. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitsarp](https://clawhub.ai/user/gitsarp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and productivity-focused users use this skill to generate a concise daily briefing from available task, meeting-note, memory, and calendar context. It helps surface overdue work, today's priorities, schedule items, recent meeting context, and one recommended focus for the day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The briefing may surface private tasks, notes, memory, or calendar details in chat. <br>
Mitigation: Use explicit briefing prompts and avoid enabling calendar or memory sources that contain information you do not want summarized. <br>
Risk: Broad trigger phrases can cause the assistant to gather more local productivity context than expected. <br>
Mitigation: Prefer clear prompts such as "daily briefing" or "run my morning briefing" and review connected data sources before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gitsarp/ai-daily-briefing-bak) <br>
- [Creator homepage](https://jeffjhunter.com) <br>
- [Quick Start](artifact/examples/quick-start.md) <br>
- [Example Output](artifact/examples/output-example.md) <br>
- [Briefing Preferences Template](artifact/assets/PREFERENCES-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown daily briefing with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize local tasks, meeting notes, memory files, and connected calendar context when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
