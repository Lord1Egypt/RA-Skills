## Description: <br>
Web crawler using breadth-first traversal and anti-scraping fallbacks to extract BBC and general news content into structured local Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felixopt17](https://clawhub.ai/user/felixopt17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content analysts use this skill to crawl BBC or other news sites, limit traversal by page count, depth, delay, and domain, and save extracted article text and images for local review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency installation runs pip and may install Playwright browser components. <br>
Mitigation: Install in a virtual environment, review requirements before installation, and avoid extra pip flags or alternate package indexes unless intentionally needed. <br>
Risk: The crawler fetches user-selected websites and writes scraped text, images, and failed URL logs to local storage. <br>
Mitigation: Use a controlled output directory, conservative max page and depth settings, adequate delay values, and review collected content before reuse. <br>
Risk: This version should not be relied on to enforce robots.txt automatically. <br>
Mitigation: Confirm site permissions and crawler rules separately before running against a target domain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felixopt17/bbccrawlermaxclaw) <br>
- [README.md](artifact/README.md) <br>
- [USAGE.md](artifact/USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown files with YAML front matter, local image files, failed URL logs, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Crawled pages are saved under date and category directories; runtime controls include URL, output directory, max pages, depth, delay, method, and allowed domains.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
