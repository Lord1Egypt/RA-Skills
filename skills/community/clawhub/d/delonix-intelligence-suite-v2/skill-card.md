## Description: <br>
德胧舆情情报综合工具箱 helps agents collect hotel-industry public-opinion signals, summarize web and video-platform findings, prepare Feishu card reports, and draft AI-assisted risk analysis and response plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoliuzhu](https://clawhub.ai/user/chaoliuzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, operations, and communications teams can use this skill to monitor hotel-brand public opinion, competitor activity, and video-platform risk signals, then turn findings into Feishu-ready summaries and mitigation plans. Agents use it as guidance for search queries, risk classification, alert thresholds, reporting formats, and automation patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation terms and recurring monitoring can collect or report information outside the intended business scope. <br>
Mitigation: Define approved monitoring topics, brands, platforms, and alert thresholds before enabling scheduled runs. <br>
Risk: Outbound Feishu reporting examples include a fixed recipient and could send sensitive monitoring results to the wrong channel. <br>
Mitigation: Replace fixed recipients with approved channels and review message routing before deployment. <br>
Risk: The skill references sensitive credentials and optional third-party packages or container images. <br>
Mitigation: Use dedicated low-privilege credentials and verify BettaFish packages or Docker images before installation. <br>
Risk: Automated monitoring jobs may continue running after the business need changes. <br>
Mitigation: Document ownership, disable procedures, and review scheduled jobs regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chaoliuzhu/delonix-intelligence-suite-v2) <br>
- [BettaFish public-opinion analysis engine](https://github.com/666ghj/BettaFish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with command examples, structured risk-analysis text, and Feishu card JSON templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include monitoring queries, alert thresholds, risk ratings, response-plan drafts, and outbound Feishu card payloads that should be reviewed before use.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
