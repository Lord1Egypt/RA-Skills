## Description: <br>
财经情报局聚合权威财经新闻源，分析利好、利空和中性信号，评估对市场、行业和公司的影响，并生成投资研究简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to collect finance news, filter by market, source, keyword, industry, or stock, and produce structured research briefings with sentiment, impact level, related securities, and suggested posture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance news summaries, keyword sentiment, and operation advice can be incomplete or misleading if treated as trading advice. <br>
Mitigation: Verify market-moving claims against primary sources and use the output as research support, not the sole basis for trades. <br>
Risk: The local script may contact public finance websites and save cache or report files locally. <br>
Mitigation: Run it in an approved network environment and review generated local files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/if530770/finance-intel) <br>
- [Sentiment rules and stock mapping](references/sentiment-rules.md) <br>
- [Finance source configuration](references/sources-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown briefings and structured JSON news records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local cache and report files under finance-news unless --no-save is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
