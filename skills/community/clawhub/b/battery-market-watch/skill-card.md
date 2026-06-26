## Description: <br>
Battery Market Watch monitors battery-market policy, regulation, safety, subsidy, and investment news across China, the United States, India, Russia, and South Korea, then generates research-style weekly reports with summaries, translations, sentiment classification, and industry interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardcoder849](https://clawhub.ai/user/richardcoder849) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and market-research users can use this skill to gather public battery-industry news, classify policy and safety signals, and produce Chinese-language Markdown and Word weekly reports for market monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to news, search, RSS, GNews, and NewsAPI providers. <br>
Mitigation: Run it in an environment where those network calls are expected, and review configured providers before execution. <br>
Risk: Optional NewsAPI and GNews credentials may be used by the search scripts. <br>
Mitigation: Set API keys only when those integrations are intended, and provide them through environment variables rather than hard-coded files. <br>
Risk: The analysis script can send prompts to a localhost LLM endpoint. <br>
Mitigation: Confirm the localhost model service is trusted and under your control before running sentiment analysis. <br>
Risk: Generated Markdown and DOCX reports may be copied to the Desktop. <br>
Mitigation: Review generated report locations and contents before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richardcoder849/battery-market-watch) <br>
- [Publisher profile](https://clawhub.ai/user/richardcoder849) <br>
- [GNews](https://gnews.io/) <br>
- [NewsAPI](https://newsapi.org/) <br>
- [U.S. Department of Energy RSS](https://www.energy.gov/rss.xml) <br>
- [U.S. EPA news RSS](https://www.epa.gov/newsreleases/search/rss.xml) <br>
- [China National Energy Administration RSS](https://www.nea.gov.cn/131053424_157526451.xml) <br>
- [China National Development and Reform Commission news](https://www.ndrc.gov.cn/xwdt/xwfb/?code=&state=123) <br>
- [India Ministry of New and Renewable Energy RSS](https://mnre.gov.in/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON, Markdown, and DOCX report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dated data files under data/ and may copy generated Markdown and DOCX reports to the user's Desktop.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
