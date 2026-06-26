## Description: <br>
A-share short-term trading decision skill for a 1-5 day horizon using real-data market sentiment, sector rotation, strong-stock scanning, capital flow confirmation, date-based signal scoring, prediction logging, and next-day market comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wu-XiaoLin](https://clawhub.ai/user/Wu-XiaoLin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze CN A-share short-term momentum candidates, generate daily market reports, log predictions, and compare those predictions with later market outcomes. Outputs are research support and should not be treated as automated trading instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-analysis outputs can be mistaken for investment advice. <br>
Mitigation: Treat outputs as research support, review recommendations before use, and require human approval before any trading action. <br>
Risk: The local data directory can record analyzed dates, signals, and candidate stocks. <br>
Mitigation: Keep generated data files private and avoid sharing decision logs outside the intended environment. <br>
Risk: The scheduler can run recurring weekday scans and reports. <br>
Mitigation: Enable scheduled jobs only when recurring scans are intended and monitor the generated outputs. <br>
Risk: Runtime depends on AkShare and pandas from the configured Python package source. <br>
Mitigation: Install dependencies only from trusted package sources and review dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Wu-XiaoLin/a-share-short-decision-bak) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Wu-XiaoLin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON objects, Markdown reports, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local decision logs under data/decision_log.jsonl when prediction logging is invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
