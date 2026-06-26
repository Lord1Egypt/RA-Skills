## Description: <br>
Analyzes CN A-share market sentiment, sector rotation, strong-stock candidates, capital flows, and risk controls to support short-term 1-5 day trading decision research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenera](https://clawhub.ai/user/kenera) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to generate CN A-share short-term market scans, daily recommendations, prediction logs, and next-day comparison reports. Outputs should be treated as automated market research and decision support, not personal financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data and dependency behavior may vary across AkShare and pandas versions, affecting reproducibility. <br>
Mitigation: Install the skill in an isolated environment and pin or review akshare and pandas versions before relying on repeated scans. <br>
Risk: Recurring scheduled scans can generate ongoing local reports and recommendations. <br>
Mitigation: Enable scheduler.yaml jobs only when recurring market scans are intended, and periodically review generated files under data/. <br>
Risk: The config optimization subskill can overwrite future screening behavior when --apply-to-config is used. <br>
Mitigation: Review optimized configuration artifacts before applying them, and avoid --apply-to-config unless persistent strategy changes are intended. <br>
Risk: Generated stock recommendations may be mistaken for personal financial advice. <br>
Mitigation: Present outputs as automated market research and decision support, and require user review before any trading decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenera/a-share-short-decision) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Scheduler configuration](artifact/scheduler.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON and Markdown reports with CLI command outputs and local data artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local reports, recommendations, optimized configuration artifacts, and prediction logs under data/.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata and config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
