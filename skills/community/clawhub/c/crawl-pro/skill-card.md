## Description: <br>
爬虫专项工作流 - 基于 Scrapling 框架的生产级采集。自适应元素定位、反爬绕过、并发规模爬取、代理轮换。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Crawl Pro to ask an agent for scraping workflow guidance, Scrapling-based crawler code, shell commands, fetcher selection, concurrency settings, and export patterns for authorized web data collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-scale scraping, stealth fetching, anti-bot bypass, and proxy rotation in contexts where the user may not have permission. <br>
Mitigation: Use it only for authorized targets and data; confirm site permission, terms, privacy basis, and allowed collection methods before running proposed crawlers. <br>
Risk: Generated crawler settings may cause excessive load or collect data too aggressively. <br>
Mitigation: Set conservative rate limits, delays, and concurrency values, and review generated code before execution. <br>
Risk: The workflow depends on Scrapling and may install or execute third-party crawling code. <br>
Mitigation: Use an isolated Python environment and pin or verify the Scrapling dependency before installing or running generated commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include crawler templates, fetcher choices, concurrency settings, checkpointing guidance, proxy-rotation configuration, and export format suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
