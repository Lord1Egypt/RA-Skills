## Description: <br>
全球热点事件监控与影响分析。覆盖全球局势、地缘冲突、重大政策、创新技术等可能影响经济、市场和投资的事件，并按行业、汇率、大宗商品链路分析影响。含定时消息推送与全渠道分段推送能力。用于 Cron 定时推送热点摘要(早8点/晚8点/整点扫描)。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market watchers use Eyes to generate concise global news summaries and market-impact analysis across politics, economics, technology, and financial markets. The skill can also support scheduled news push workflows for configured chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create scheduled outbound news summaries to configured chat channels. <br>
Mitigation: Confirm the destination channel and target before installation, and review the created cron jobs after setup. <br>
Risk: Server security evidence flags under-disclosed fallback targeting and promotional message behavior. <br>
Mitigation: Review or disable the BigA fallback and promotional message behavior before use in shared or commercial channels. <br>
Risk: Recurring jobs may continue sending messages after the initial setup. <br>
Mitigation: Document how to list, edit, and remove the Eyes cron jobs before enabling scheduled delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kobenfang/eyes) <br>
- [cron-install-shell.sh](references/cron-install-shell.sh) <br>
- [cron-templates.json](references/cron-templates.json) <br>
- [event-impact-matrix.md](references/event-impact-matrix.md) <br>
- [user-preferences.md](references/user-preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce segmented outbound channel messages and scheduled OpenClaw cron configuration when the user enables those workflows.] <br>

## Skill Version(s): <br>
5.3.12 (source: server release metadata; artifact _meta.json reports 5.3.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
