## Description: <br>
Builds a forward-looking market catalyst calendar covering macro policy, earnings, industry policy, and market technical events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzy11650](https://clawhub.ai/user/dzy11650) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance-focused users and agents use this skill to scan upcoming events over a selected time window, classify their likely market impact, and produce a concise calendar with investor-facing follow-up guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent IMA reminder notes for high-impact events without a clear opt-in step. <br>
Mitigation: Require user confirmation before creating IMA reminders and review generated notes before relying on them. <br>
Risk: Forward-looking market catalysts and investor suggestions may be incomplete, stale, or based on expectations that change quickly. <br>
Mitigation: Verify event sources and market assumptions before making investment or risk-management decisions. <br>


## Reference(s): <br>
- [Catalyst Calendar on ClawHub](https://clawhub.ai/dzy11650/catalyst-calendar) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown report with event tables, a weekly timeline, investor response suggestions, and IMA reminder notes for high-impact events.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under catalyst-calendar/reports/YYYY-MM-DD-catalyst-calendar.md; 14-day reports are capped at 800 characters, 30-day reports at 1200 characters, and each day has at most three high-impact events.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and README version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
