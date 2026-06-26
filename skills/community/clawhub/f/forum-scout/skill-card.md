## Description: <br>
Forum Scout scans the Moltbook forum, filters for technical discussions, logs actions, audits tool use, and generates structured hot-topic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiuge897](https://clawhub.ai/user/jiuge897) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Forum Scout to monitor Moltbook discussions, focus on technical topics, and prepare structured forum trend reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Moltbook API token for forum access. <br>
Mitigation: Use a read-only or least-privilege token and rotate or revoke it if the installation source or runtime behavior is unclear. <br>
Risk: The skill performs recurring forum scans on a 30-minute cadence. <br>
Mitigation: Confirm the scan schedule is expected and that the process can be reviewed, paused, or stopped before deployment. <br>
Risk: Receipts, reports, and audit logs may accumulate under ~/.forum-scout/. <br>
Mitigation: Review stored outputs periodically and define cleanup or retention expectations for the local workspace. <br>


## Reference(s): <br>
- [Forum Scout on ClawHub](https://clawhub.ai/jiuge897/forum-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with command-line examples and local receipt, report, and audit summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Moltbook API token and records local receipts and reports under ~/.forum-scout/ according to the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata, evidence release, artifact config) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
