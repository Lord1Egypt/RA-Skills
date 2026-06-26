## Description: <br>
Generates and sends daily work summaries from workspace notes using a configurable Markdown template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rare](https://clawhub.ai/user/rare) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Employees and agent operators use this skill at end of day to compile a work summary from daily memory, optional conversation or task context, and a report template, then save or deliver it to configured channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read private workspace memory, conversations, or task status while building a report. <br>
Mitigation: Keep conversation logs and task status opt-in, and preview or redact sensitive report content before scheduled runs. <br>
Risk: Reports can be sent to external messaging services or incorrect channel targets. <br>
Mitigation: Configure only trusted delivery targets and require review before multi-channel or scheduled sends. <br>


## Reference(s): <br>
- [Daily Report Skill on ClawHub](https://clawhub.ai/rare/daily-report-skill) <br>
- [Config Example](references/config.example.md) <br>
- [Daily Report Template](assets/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Configuration, API calls] <br>
**Output Format:** [Markdown report generated from a template, optionally delivered through configured messaging channels] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes memory/daily-reports/YYYY-MM-DD.md and can send the report to configured channels.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
