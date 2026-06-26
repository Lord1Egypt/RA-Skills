## Description: <br>
Scrape e-commerce homepages from multiple websites in a target market, handle popups automatically, capture screenshots and HTML, extract product data, and generate comprehensive market analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nepp-an](https://clawhub.ai/user/nepp-an) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Market researchers, business analysts, and e-commerce operators use this skill to gather homepage screenshots and HTML from target-market retail sites, extract product and price signals, and produce market analysis reports. It supports competitor research, product trend analysis, price comparison, and localized market-entry planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Playwright scraper that visits third-party websites, clicks consent or popup controls, and writes screenshots plus raw HTML to disk. <br>
Mitigation: Use explicit target-site lists, avoid authenticated or personal pages, review website terms before scraping, and inspect generated local artifacts before sharing. <br>
Risk: The security review notes anti-bot evasion guidance and broad auto-activation language. <br>
Mitigation: Review the skill before installation and do not use anti-bot evasion or proxy-rotation guidance without proper authorization. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nepp-an/ecommerce-market-analyzer-skill) <br>
- [Popup patterns](references/popup_patterns.md) <br>
- [HTML parsing patterns](references/html_parsing_patterns.md) <br>
- [Market analysis report template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, generated screenshots, saved HTML files, and market analysis reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local screenshot and HTML artifacts for each configured website before generating a report.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
