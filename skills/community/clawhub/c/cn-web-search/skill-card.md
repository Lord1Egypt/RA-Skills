## Description: <br>
Chinese web search skill that helps agents query public search engines and websites for Chinese, English, WeChat, finance, technical, macroeconomic, U.S. stock, sentiment, and Pre-IPO information without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joansongjr](https://clawhub.ai/user/joansongjr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to compose web-fetch searches across multiple public Chinese, English, finance, technical, macroeconomic, sentiment, and IPO sources. It is suited for gathering current public web results that should be reviewed and cross-checked before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to external public search engines and websites. <br>
Mitigation: Do not include secrets, credentials, private company data, personal data, or regulated information in queries. <br>
Risk: Fetched web content can be incomplete, stale, or untrusted. <br>
Mitigation: Verify important results against authoritative sources before relying on them for decisions. <br>
Risk: Server evidence reports unavailable provenance and notes inconsistent visible metadata. <br>
Mitigation: Verify the installed version and publisher before using the skill where provenance matters. <br>


## Reference(s): <br>
- [CN Web Search on ClawHub](https://clawhub.ai/joansongjr/cn-web-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with URL templates and web_fetch command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search queries may be sent to external public search engines and websites.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
