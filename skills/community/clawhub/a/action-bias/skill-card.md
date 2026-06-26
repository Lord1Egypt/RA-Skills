## Description: <br>
Action Bias helps developers and operators restructure agent prompts and recurring shifts so agents produce externally visible actions with proof instead of report-only output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crewhaus](https://clawhub.ai/user/crewhaus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn report-producing prompts, cron jobs, and agent shifts into action-oriented workflows that require outbound work and proof of completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to perform outward-facing work, including emails, public posts, repository pushes, API writes, and directory submissions. <br>
Mitigation: Use scoped accounts and tools, and require human approval before emails, public posts, code pushes, production API writes, or directory submissions. <br>
Risk: Action logs may contain contact details, URLs, post IDs, response codes, or other operational evidence. <br>
Mitigation: Protect action logs, minimize stored personal data, and avoid exposing logs beyond the team that needs them. <br>
Risk: Broad action-first instructions can push agents beyond the intended business or safety scope. <br>
Mitigation: Define allowed destinations, repositories, APIs, accounts, and action categories before using the skill. <br>


## Reference(s): <br>
- [Action Bias ClawHub Page](https://clawhub.ai/crewhaus/action-bias) <br>
- [Action Audit Guide](references/action-audit.md) <br>
- [Shift Restructuring Guide](references/shift-restructuring.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, checklists, and inline command placeholders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request or recommend outward-facing actions such as emails, public posts, repository pushes, API writes, and directory submissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
