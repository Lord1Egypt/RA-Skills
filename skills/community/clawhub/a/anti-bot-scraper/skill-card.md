## Description: <br>
Anti-Bot Scraper is a Playwright-based web scraping skill with simple, stealth, and batch modes for extracting page text, links, images, metadata, screenshots, and HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tttyix](https://clawhub.ai/user/tttyix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Playwright scrapers against permitted web targets, extract structured page content, and optionally save screenshots or HTML for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stealth scraping, proxies, and fingerprint changes can be used to evade access controls or site rules. <br>
Mitigation: Use the skill only on targets where scraping is permitted, and do not use stealth or proxy features to bypass restrictions. <br>
Risk: Saved HTML, screenshots, or authenticated cookies may expose private or account-linked data. <br>
Mitigation: Avoid real account cookies unless necessary, review saved captures promptly, and delete sensitive outputs after use. <br>
Risk: Batch scraping can create excessive traffic to target sites. <br>
Mitigation: Keep concurrency low and scope URL lists to authorized collection tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tttyix/anti-bot-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Files, Shell commands] <br>
**Output Format:** [JSON to stdout with optional screenshot, HTML, or JSON output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Simple and stealth modes return one scrape result; batch mode can process multiple URLs with configurable concurrency.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
