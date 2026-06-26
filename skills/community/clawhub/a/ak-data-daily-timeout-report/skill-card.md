## Description: <br>
Unified daily timeout entry for AK Data single job type: task timeout + crawler timeout + comparison + drill-down examples with log request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leehoo29](https://clawhub.ai/user/leehoo29) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and data engineering users use this skill to generate daily and trend reports comparing AK Data task timeouts with crawler timeouts for a selected job type. It also supports drill-down examples that include log request details for follow-up investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can include raw request payloads or customer/internal identifiers from database logs. <br>
Mitigation: Restrict access to generated reports and avoid sharing outputs outside the intended operational audience. <br>
Risk: The skill depends on external Python scripts and database credentials that are not included in the artifact. <br>
Mitigation: Review the referenced scripts before use, keep .env secrets out of version control, and use a read-only database account with the narrowest practical access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leehoo29/ak-data-daily-timeout-report) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Migration Guide](artifact/MIGRATION.md) <br>
- [Template Migration Notes](artifact/TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON or Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include task samples, log state, and request payload excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
