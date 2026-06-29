## Description: <br>
Smart Web Search helps agents run region-aware web searches and optionally fetch result-page content across China and international networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to search the web, collect ranked results, and optionally fetch page text for research, troubleshooting, and content discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, IP/network metadata, and fetched result URLs are sent to search engines, geolocation services, and result websites. <br>
Mitigation: Avoid sensitive searches, disable or reduce automatic fetching when possible, and use explicit search requests when privacy matters. <br>
Risk: Fetched page content may be incomplete, outdated, or shaped by search-engine and result-site behavior. <br>
Mitigation: Review returned URLs and fetched content before relying on them for decisions, citations, or downstream skill changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ucsdzehualiu/free-smart-web-search) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and fetched page-content text, with setup and usage guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count, automatic page fetching, maximum fetched text length, and regional search routing are configurable by command options.] <br>

## Skill Version(s): <br>
2.0.0 (source: server evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
