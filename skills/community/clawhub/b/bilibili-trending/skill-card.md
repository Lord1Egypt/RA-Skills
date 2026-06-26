## Description: <br>
获取 Bilibili 全榜单热门数据并分析趋势。支持 21 个榜单，自动调用子 Agent 分析并生成 MD 报告持久化储存。安全无隐私风险，仅调用公开 API。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rookiecoder-jsjs](https://clawhub.ai/user/rookiecoder-jsjs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect public Bilibili ranking data, generate trend summaries, and produce Chinese Markdown reports for category, keyword, creator, and anomaly analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes Bilibili ranking history, reports, and alerts into the configured workspace. <br>
Mitigation: Set BILIBILI_WORKSPACE deliberately and review generated json/ and memory/bilibili-analysis/ files before sharing or committing them. <br>
Risk: The default workflow can send fetched public ranking data to an OpenClaw sub-agent for analysis. <br>
Mitigation: Use --manual mode when you want to inspect the generated prompt or avoid spawning a sub-agent. <br>
Risk: Frequent Bilibili API requests may be rate limited or fail during daemon collection. <br>
Mitigation: Use reasonable daemon intervals and rely on the built-in retry and backoff behavior rather than aggressive polling. <br>


## Reference(s): <br>
- [Bilibili analysis workflow](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/rookiecoder-jsjs/bilibili-trending) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON data files, text alerts, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes ranking data under json/ and analysis reports, trend history, and alerts under memory/bilibili-analysis/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
