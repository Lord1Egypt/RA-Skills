## Description: <br>
输入ASIN，自动抓取数百条评论，AI逐条深度打标，生成痛点/卖点/Listing优化洞察报告。支持RapidAPI数据采集、OpenAI/DeepSeek兼容API、交互式HTML报告输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, marketers, and product teams use this skill to analyze Amazon reviews from an ASIN and turn them into pain points, selling points, user profiles, and listing optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review text, product metadata, and selected LLM API keys may be sent to configured external providers. <br>
Mitigation: Use trusted API providers and api_base values, avoid confidential business notes in prompts, and use mock or local modes for testing when external sharing is not acceptable. <br>
Risk: Fetched review text is inserted into an auto-opened HTML report without evident escaping. <br>
Mitigation: Inspect generated reports before sharing or relying on them, and treat reports from live review data as untrusted local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/amazon-review-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/bettermen) <br>
- [RapidAPI Amazon hub](https://rapidapi.com/hub/amazon) <br>
- [OpenAI-compatible API endpoint](https://api.openai.com/v1) <br>
- [DeepSeek API endpoint](https://api.deepseek.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ASIN and LLM API key; can use RapidAPI for live review data or mock modes for testing.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
