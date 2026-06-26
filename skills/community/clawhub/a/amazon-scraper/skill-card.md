## Description: <br>
High-performance containerized Amazon scraper using Docker, Playwright Extra, and the Stealth plugin to collect Amazon best-seller, search-result, product-detail, and generic dynamic-page data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafar](https://clawhub.ai/user/jiafar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to run containerized scraping workflows for Amazon product research, category ranking, search-result extraction, product-detail extraction, and limited generic webpage text capture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the skill suspicious because it combines broad web scraping, stealth browser automation, and bundled third-party proxy credentials. <br>
Mitigation: Install only for authorized scraping, review target-site terms and data-handling obligations, and replace or remove bundled proxies before use. <br>
Risk: The skill can retrieve arbitrary web content and write JSON outputs to a mounted directory. <br>
Mitigation: Avoid private, internal, or sensitive URLs and keep scraper outputs in a dedicated mounted directory with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiafar/amazon-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scraper runtime outputs JSON to stdout or a mounted output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Amazon mode returns product records with fields such as rank, title, ASIN, price, rating, review count, image URL, product URL, BSR, and bought-past-month when available; generic mode returns page title and body text capped at 10000 characters.] <br>

## Skill Version(s): <br>
3.4.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
