## Description: <br>
Behavioral cost coach for OpenClaw fleets. Analyzes your sessions, shows what you did that cost money, and coaches you on what to do differently. Finds both technical waste (wrong model, no tool budget) and behavioral waste (blind retries, over-scheduled crons). Run daily via cron or trigger manually. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nabilrehman](https://clawhub.ai/user/nabilrehman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and teams running OpenClaw fleets use ClawDoctor to review session costs, identify expensive usage habits, and produce cost-saving recommendations or configuration fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent OpenClaw session transcripts, which may contain private operational or user data. <br>
Mitigation: Install only in environments where transcript access is acceptable, and review the scope of session data before running analysis. <br>
Risk: The skill can apply live fleet configuration changes from broad conversational approvals. <br>
Mitigation: Require explicit approval for the affected agents, exact patch payload, expected savings, and rollback steps before applying a fix. <br>
Risk: The skill saves local cost-analysis state and pending fixes. <br>
Mitigation: Protect the workspace state files and review them for sensitive cost or fleet information before sharing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nabilrehman/clawdoctor) <br>
- [Publisher profile](https://clawhub.ai/user/nabilrehman) <br>
- [Faan AI](https://faan.ai) <br>
- [Report Formats](references/report-formats.md) <br>
- [Fix Payloads & Model Tiers](references/fix-payloads.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local analysis state and pending fix records after reviewing OpenClaw fleet and session data.] <br>

## Skill Version(s): <br>
4.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
