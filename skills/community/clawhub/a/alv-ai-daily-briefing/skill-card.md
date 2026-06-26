## Description: <br>
Start every day focused with a morning briefing that summarizes overdue tasks, today's priorities, calendar events, and context from recent meetings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual users use this skill to start the day with a concise briefing across tasks, meeting notes, calendar items, and personal context. It helps identify overdue work, immediate priorities, and one recommended focus for the day. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to read and summarize private task, meeting, memory, profile, and calendar information. <br>
Mitigation: Use it only in workspaces where that data may be summarized, and review connected sources before requesting a briefing. <br>
Risk: Server metadata includes crypto and purchase capability tags that do not match the instruction-only briefing behavior. <br>
Mitigation: Verify the runtime does not grant unrelated crypto or purchase permissions before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/alvisdunlop/alv-ai-daily-briefing) <br>
- [Creator homepage](https://jeffjhunter.com) <br>
- [Quick Start](examples/quick-start.md) <br>
- [Example Output](examples/output-example.md) <br>
- [Briefing Preferences Template](assets/PREFERENCES-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefing with structured sections, bullets, and optional checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize workspace to-do lists, recent meeting notes, memory/profile files, and connected calendar data when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
