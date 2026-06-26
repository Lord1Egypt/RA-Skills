## Description: <br>
Generates an A-share daily market review report and can optionally send it by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnxufei-tech](https://clawhub.ai/user/cnxufei-tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to create daily A-share market recaps with market overview, leaderboards, sentiment signals, and next-day strategy notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMTP email delivery can expose account credentials if a personal password is reused or stored unsafely. <br>
Mitigation: Use a dedicated SMTP or app password from an environment variable and avoid committing email configuration with secrets. <br>
Risk: Date text copied into shell commands could lead to unintended command execution if it is not trusted. <br>
Mitigation: Validate date inputs and use only the supported YYYYMMDD, YYYY-MM-DD, or omitted-date forms before running the command. <br>
Risk: External AkShare data sources can be intermittently unavailable, which may affect report completeness. <br>
Mitigation: Review generated reports before sharing or trading on them, and rely on the skill's documented retry and fallback behavior only as a resilience aid. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnxufei-tech/daily-review-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report file with optional SMTP email delivery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves reports to stock-analysis/reports/YYYYMMDD.md; accepts YYYYMMDD, YYYY-MM-DD, or today's date when omitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
