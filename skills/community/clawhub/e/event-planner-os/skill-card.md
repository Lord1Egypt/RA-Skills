## Description: <br>
A conversational OpenClaw skill for planning and managing events from start to finish, including tasks, timelines, vendors, volunteers, budgets, and built-in planning templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan and track events of many sizes, from dinner parties to conferences, by maintaining event records, task checklists, vendor details, volunteer assignments, and budgets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores event details, contacts, vendors, helpers, and budgets in a local event-data.json file. <br>
Mitigation: Avoid entering sensitive contact or budget details unless local storage is acceptable, and review or delete event-data.json when saved planning data is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris-openclaw/event-planner-os) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [Evaluation scenarios](artifact/evals/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with persisted structured JSON event data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists event records, task lists, vendor details, volunteer assignments, and budgets in event-data.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
