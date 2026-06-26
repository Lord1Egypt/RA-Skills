## Description: <br>
Bug Hunter helps developers and QA teams analyze logs, stack traces, screenshots, and API errors to identify likely root causes and produce structured bug reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhanghengyi1986-afk](https://clawhub.ai/user/zhanghengyi1986-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and support teams use this skill to triage bugs, interpret error evidence, classify severity and priority, and draft actionable bug reports with reproduction steps, expected results, actual results, and supporting evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debug logs and API troubleshooting artifacts may contain Authorization headers, cookies, tokens, API keys, passwords, session IDs, customer data, or sensitive request and response fields. <br>
Mitigation: Redact secrets and sensitive data before saving, sharing, or attaching diagnostic artifacts, and use approved storage for retained evidence. <br>
Risk: The skill can guide users to capture full API request and response details for bug reports. <br>
Mitigation: Prefer sanitized examples, omit unnecessary payload fields, and verify that any included request or response evidence is approved for the audience receiving the bug report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhanghengyi1986-afk/bug-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown bug reports, triage notes, analysis tables, and optional shell-command snippets for log inspection.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable bug analysis and report content for an agent to adapt to the target issue and environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
