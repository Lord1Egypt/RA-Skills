## Description: <br>
Copy a public figure's thinking into a callable thinking skill for a given scenario by extracting and replicating their thinking style, mental models, reasoning, and decision logic rather than merely imitating tone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runshengdu](https://clawhub.ai/user/runshengdu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Copy Brain to research a public figure's public materials and generate a reusable persona-style thinking skill for a specified decision scenario. The skill helps an agent reason using documented mental models and decision criteria while preserving source links and review notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send persona names, scenario terms, and URLs to Tavily, ScrapeBadger, or RedFox when those services are configured. <br>
Mitigation: Do not include confidential names, private investigation terms, secrets, or sensitive URLs in searches; install only when third-party research API use is acceptable. <br>
Risk: Generated persona skills can influence future agent reasoning and may overstate how closely they represent a real person's views. <br>
Mitigation: Review the generated persona skill before reuse, keep source links with factual claims, and make clear that the result is a public-source simulation rather than the actual person. <br>
Risk: The skill requires optional API credentials for broader research coverage. <br>
Mitigation: Provide credentials through environment variables only and avoid writing API keys into prompts, generated files, logs, or shared artifacts. <br>


## Reference(s): <br>
- [Tavily Search API Documentation](https://docs.tavily.com/documentation/api-reference/endpoint/search) <br>
- [ScrapeBadger API Documentation](https://docs.scrapebadger.com/api-reference/introduction) <br>
- [RedFox WeChat Official Account Search API](https://redfox.hk/apis/gongzhonghao/PW97QFBS) <br>
- [RedFox WeChat Official Account Work API](https://redfox.hk/apis/gongzhonghao/XEO0QQNF) <br>
- [RedFox Xiaohongshu Search API](https://redfox.hk/apis/xiaohongshu/384C6W6B) <br>
- [RedFox Xiaohongshu Detail API](https://redfox.hk/apis/xiaohongshu/KR1LPTBF) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown persona skill file with frontmatter, source notes, and optional shell commands for research helpers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a user-confirmed persona skill under output/ and can call optional third-party research APIs when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
