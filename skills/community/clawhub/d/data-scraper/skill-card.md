## Description: <br>
Web page data collection and structured text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to fetch public or clearly authorized web pages, extract readable text or simple structured data, and create scrape-result events for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping unauthorized, private, or internal URLs can expose sensitive content or violate site terms. <br>
Mitigation: Use the skill only on public or clearly authorized pages, avoid internal/private URLs, and respect applicable site policies. <br>
Risk: Cookies, bearer tokens, or other credentials supplied for scraping can be exposed to untrusted target domains. <br>
Mitigation: Provide credentials only for trusted domains and avoid passing authentication material unless it is required and approved. <br>
Risk: Scraped URLs and content may be persisted in local scrape-result events or memory files. <br>
Mitigation: Review and delete stored scrape events or memory files when URLs or page contents are sensitive. <br>
Risk: Some documented safeguards and modes may require implementation beyond the supplied run.sh. <br>
Mitigation: Verify batch scraping, robots.txt handling, retry, and watch behavior before relying on those safeguards. <br>


## Reference(s): <br>
- [Data Scraper ClawHub Page](https://clawhub.ai/mupengi-bot/data-scraper) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [User Guide](artifact/GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, HTML, JSON, Markdown, Shell commands, Files] <br>
**Output Format:** [Plain text or HTML on stdout, with JSON scrape-result event files; documentation also describes JSON, CSV, and Markdown table outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches URLs with curl, optionally converts HTML to text, and writes local scrape-result event files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
