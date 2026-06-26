## Description: <br>
Auto Weekly Report System collects weekly v3.5, InStreet, price monitoring, and system health data, generates a Markdown report, and prepares publication to WeCom documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect local operational signals, produce a weekly Markdown report, and prepare a WeCom document publication workflow for team reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads named local files under /tmp and may summarize operational data into a weekly report. <br>
Mitigation: Run it only in environments where those /tmp files are intended report inputs, and review /tmp/weekly_report_auto.md before sharing it. <br>
Risk: Publishing guidance prepares WeCom document commands that can expose report contents to an unintended account or audience. <br>
Mitigation: Confirm the WeCom account, document target, and visibility settings before executing generated publication commands. <br>
Risk: The quick-start documentation references generate_weekly.py, while the artifact contains generator.py. <br>
Mitigation: Use the included full_pipeline.py or generator.py entry points, and correct local runbooks before scheduling cron jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/auto-weekly-report-system) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/rf-ai-wh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes weekly data, report, and publication command files under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
