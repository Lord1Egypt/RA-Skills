## Description: <br>
Designer intelligence collection tool that monitors public AI, hardware, mobile, and design sources, applies dynamic quality filtering, and generates structured daily and weekly reports with local data storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15217172098](https://clawhub.ai/user/15217172098) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, product teams, and design leaders use this skill to collect public industry intelligence across AI, hardware, mobile, and design sources, filter it by designer-focused criteria, and produce daily or weekly Markdown briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional social-media setup can involve browser cookies or logged-in sessions, which conflicts with the local-only and no-login posture described elsewhere. <br>
Mitigation: Disable or avoid Twitter/X and Xiaohongshu sources unless the operator intentionally wants to use those sessions, and review the source list before installation. <br>
Risk: Report-sending examples may target a fixed recipient or unintended message channel. <br>
Mitigation: Verify the recipient and destination channel before sending any generated report. <br>
Risk: Scheduled execution can repeatedly fetch external sources and generate local outputs without manual review. <br>
Mitigation: Run the skill manually in a virtual environment before enabling cron or other automation. <br>
Risk: Generated reports and cache files may contain sensitive working context if stored in shared temporary locations. <br>
Mitigation: Use a private output directory instead of /tmp for confidential or organization-specific material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15217172098/designer-intelligence-station) <br>
- [Execution flow documentation](docs/execution-flow.md) <br>
- [Output format specification](docs/format-spec.md) <br>
- [Screening guide](docs/screening-guide.md) <br>
- [Auto-send guide](docs/auto-send-guide.md) <br>
- [Default source list](data/default_sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with tables and links; local JSON and SQLite data files; shell commands for setup and scheduled execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily and weekly briefings, optional cron-based scheduling, and local cache/output paths under data/cache/ and temp/.] <br>

## Skill Version(s): <br>
2.1.8 (source: server release metadata, SKILL.md frontmatter, package.json, _meta.json, CHANGELOG released 2026-04-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
