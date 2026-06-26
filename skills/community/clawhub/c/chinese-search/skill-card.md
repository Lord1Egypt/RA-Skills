## Description: <br>
Chinese Search helps agents produce curl-based Chinese web search commands for Bing China, Sogou WeChat, and related Chinese search workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Chinese-language web content, WeChat public articles, market research, content ideas, and technical documentation using direct search-engine queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to third-party public search engines and may be logged by those providers. <br>
Mitigation: Avoid using secrets, internal project names, regulated data, or sensitive personal information as search queries. <br>
Risk: Public search endpoints can apply rate limits, scraping restrictions, bot detection, or provider-specific access policies. <br>
Mitigation: Use conservative request rates, respect provider terms, and prefer official APIs for commercial or high-volume usage. <br>
Risk: Search responses are HTML pages that can change structure or require additional headers, cookies, JavaScript rendering, or manual parsing. <br>
Mitigation: Validate returned results before relying on them and update parsing or request headers when providers change behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaising-openclaw1/chinese-search) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Quickstart Guide](artifact/QUICKSTART.md) <br>
- [Test Results](artifact/TEST-RESULTS.md) <br>
- [Bing China Search](https://cn.bing.com/search) <br>
- [Sogou WeChat Search](https://weixin.sogou.com/weixin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and returns third-party search engine HTML that may need parsing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
