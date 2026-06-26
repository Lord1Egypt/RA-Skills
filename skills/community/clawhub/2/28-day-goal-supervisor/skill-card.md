## Description: <br>
GrowthLoop helps users refine habit goals, break them into daily plans, track check-ins, adjust difficulty, receive reminders, and view progress across up to five habits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chestnuuutli](https://clawhub.ai/user/chestnuuutli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a personal habit coach to turn goals into practical daily routines, record progress, receive check-in reminders, and review habit summaries or visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores habit history locally, which may include sensitive personal routines or notes. <br>
Mitigation: Use the configured local data directory intentionally and avoid entering secrets or sensitive personal details in habit notes. <br>
Risk: Reminder checks may surface habit status during conversations or through external schedulers. <br>
Mitigation: Enable cron, webhooks, or other external reminder schedulers only when automated reminders are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chestnuuutli/28-day-goal-supervisor) <br>
- [Publisher profile](https://clawhub.ai/user/chestnuuutli) <br>
- [Coaching style guide](references/coaching_style.md) <br>
- [Edge case handling guide](references/edge_cases.md) <br>
- [Plan generation rules](references/plan_generation_rules.md) <br>
- [Goal rationalization guide](references/rationalization_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples, JSON command responses, text summaries, and optional SVG visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores habit history locally in a JSON file and can provide reminder configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
