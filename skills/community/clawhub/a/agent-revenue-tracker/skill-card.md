## Description: <br>
Revenue Tracker helps autonomous agents log revenue events, track MRR, assets, trades, acquisition channels, goals, and learning metrics, and generate ASCII or HTML dashboards plus structured update instructions for Google Sheets, Notion, and Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of autonomous-agent workflows use this skill to maintain an agent-managed revenue ledger, monitor income streams and financial goals, and produce dashboard or report outputs for routine business review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive revenue details may be persisted in workspace files and prepared for Google Sheets, Notion, or Telegram updates without clear approval controls. <br>
Mitigation: Set exact approved destinations, require confirmation before external sync or alerts, use limited-purpose accounts, and avoid client names or secrets in descriptions. <br>
Risk: Strict workspace confinement may be affected by logging paths that need explicit review. <br>
Mitigation: Review and fix logging path declarations and permissions before deployment when confinement matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/georges91560/agent-revenue-tracker) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, ASCII dashboards, HTML reports, and JSON or JSONL ledger files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes revenue state, events, assets, goals, reports, audit entries, and learning logs under workspace paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and README mention 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
