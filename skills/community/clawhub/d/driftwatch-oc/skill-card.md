## Description: <br>
Scan your OpenClaw workspace for truncation risks, compaction anchor health, workspace hygiene, and drift tracking over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danandbub](https://clawhub.ai/user/danandbub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use Driftwatch to scan workspace bootstrap files for truncation risk, compaction anchor health, hygiene issues, and growth trends before those issues affect agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports and saved scan history can reveal local workspace details. <br>
Mitigation: Treat reports and history under ~/.driftwatch as private diagnostics and review them before sharing in chat or with teammates. <br>
Risk: Enabling --save or cron monitoring creates ongoing local records of workspace health. <br>
Mitigation: Enable persistent history or cron monitoring only when ongoing local records are intended. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/danandbub/driftwatch-oc) <br>
- [Publisher profile](https://clawhub.ai/user/danandbub) <br>
- [Bub Builds homepage](https://bubbuilds.com) <br>
- [README](README.md) <br>
- [OpenClaw constants](references/constants.py) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Conversational summary with optional JSON, HTML report files, cron summary lines, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal scans exit 0 and produce JSON for agent interpretation; --check mode can emit one-line status with non-zero warning or critical exit codes.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
