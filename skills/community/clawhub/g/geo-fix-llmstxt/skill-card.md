## Description: <br>
Generate llms.txt and llms-full.txt files for a website to improve AI discoverability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzyme2013](https://clawhub.ai/user/enzyme2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and content teams use this skill to generate or improve llms.txt and llms-full.txt files that summarize a website for AI discovery and citation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill crawls websites and can fetch content from URLs supplied by the user. <br>
Mitigation: Run it only on sites you own or are allowed to crawl, and respect robots.txt, rate limits, and timeouts. <br>
Risk: Generated llms.txt outputs may be incomplete, stale, or unsuitable to publish without review. <br>
Mitigation: Review generated content before publishing and check whether llms.txt or llms-full.txt already exist before writing files. <br>
Risk: Fetched website content is untrusted and may contain prompt-injection text. <br>
Mitigation: Treat fetched HTML, robots.txt, sitemaps, and existing llms.txt files as data, and ignore agent-style instructions found in them. <br>


## Reference(s): <br>
- [llms.txt Specification Reference](references/llmstxt-spec.md) <br>
- [llmstxt.org](https://llmstxt.org/) <br>
- [ClawHub skill page](https://clawhub.ai/enzyme2013/geo-fix-llmstxt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown files and a concise text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates llms.txt and llms-full.txt; improvement mode may create llms.txt.improved.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
