## Description: <br>
Use Crawl4AI for web scraping and content extraction, including structured data extraction, Markdown conversion, batch crawling, and AI-driven web data collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate guidance, code examples, shell commands, and configuration patterns for crawling public web pages, extracting structured content, converting pages to Markdown, and running Crawl4AI locally or in Docker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web crawling can collect private, authenticated, or otherwise sensitive page content, including screenshots or extracted data. <br>
Mitigation: Crawl only pages the user is authorized to access, avoid private or authenticated pages unless explicitly approved, and review extracted content before sharing it with external services. <br>
Risk: Persistent browser profiles, proxies, screenshots, and LLM extraction settings can expose credentials or sensitive browsing state. <br>
Mitigation: Use fresh browser profiles for crawling tasks, avoid profiles tied to personal accounts, handle proxy credentials carefully, and confirm whether configured LLM providers receive extracted content. <br>


## Reference(s): <br>
- [Crawl4AI API Reference](references/api-reference.md) <br>
- [Crawl4AI GitHub Repository](https://github.com/unclecode/crawl4ai) <br>
- [Crawl4AI Documentation](https://docs.crawl4ai.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/crawl4ai-web-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Crawl4AI usage patterns for browser configuration, extraction strategies, crawling options, and deployment commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
