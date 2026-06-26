## Description: <br>
Multi-agent adversarial debate system with 4 roles (Pro, Con, Judge, Orchestrator), per-round evidence refresh, 5-element reasoning chains, and structured bilingual Markdown report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwxga](https://clawhub.ai/user/xwxga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run adversarial multi-perspective debates, red-team a topic, refresh and verify evidence, maintain a claim ledger, and produce structured final reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional scheduled refresh can persistently rerun networked evidence refreshes and change reports after the original session ends. <br>
Mitigation: Enable any cron job only after inspecting the exact command, documenting where it is installed, and confirming a clear disable or removal path. <br>
Risk: The workflow searches and fetches web evidence, so unreliable, stale, or contradictory sources can affect debate outputs. <br>
Mitigation: Use the built-in freshness checks, source credibility labels, cross-source verification, and judge audit outputs before relying on a final report. <br>
Risk: Helper scripts and local agent CLI calls create and mutate workspace files during debate orchestration. <br>
Mitigation: Run the skill in a dedicated workspace, review generated files and audit logs, and inspect helper scripts before commercial deployment. <br>


## Reference(s): <br>
- [Data Contracts](references/data-contracts.md) <br>
- [Quick Start](examples/quickstart.md) <br>
- [Critical Debater homepage](https://github.com/xwxga/critical-debater) <br>
- [ClawHub skill page](https://clawhub.ai/xwxga/critical-debater) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, structured JSON files, and shell commands for local debate workspaces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local workspace files for evidence, claims, rounds, reports, and audit logs.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
