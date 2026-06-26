## Description: <br>
Ai Daily Briefing produces a morning briefing with overdue tasks, today's priorities, calendar overview, and recent meeting context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused agents use this skill to assemble a daily overview from local to-do items, recent meeting notes, memory/context files, and available calendar data so the user can start the day with clear priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases can cause the agent to read sensitive local task lists, recent meeting notes, memory/context files, and calendar entries without explicit per-source confirmation. <br>
Mitigation: Invoke the skill with explicit daily-briefing prompts and enable only the local sources intended for the briefing. <br>
Risk: The generated briefing may consolidate personal or confidential schedule, task, and meeting details into one response. <br>
Mitigation: Use the briefing in trusted contexts and review or redact sensitive details before sharing the output. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/alvisdunlop/alvis-ai-daily-briefing) <br>
- [Creator homepage](https://jeffjhunter.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown daily briefing with task lists and short prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-message briefing; skips empty sections and limits most sections to five items except calendar.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
