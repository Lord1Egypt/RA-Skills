## Description: <br>
Extracts clean Markdown content from user-provided URLs, including JavaScript-rendered single-page apps and concurrent multi-URL scraping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch web pages that the user identifies and save or inspect cleaned Markdown, links, JSON, screenshots, or raw page content. It is intended for static pages and JavaScript-rendered pages, with guidance to escalate to browser interaction only when scraping is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ad hoc npx execution can run an unpinned Firecrawl CLI version. <br>
Mitigation: Prefer a verified or pinned Firecrawl CLI before allowing an agent to run scrape commands. <br>
Risk: Scraping private or authenticated pages can process and save sensitive content locally. <br>
Mitigation: Use the skill only for URLs the user intends to process, and avoid private or authenticated pages unless local storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/firecrawl-scrape-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may write local Markdown or JSON files under .firecrawl when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version text) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
