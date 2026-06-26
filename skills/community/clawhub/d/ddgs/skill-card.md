## Description: <br>
Perform privacy-focused web searches via DDGS metasearch for webpages, news, images, videos, or books with no tracking and no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idkwhodatis](https://clawhub.ai/user/idkwhodatis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current search results, news, images, videos, and books through DDGS with configurable region, safe-search, time limit, and result-count parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and related network metadata are sent to external search services or configured proxies. <br>
Mitigation: Do not search for secrets, credentials, confidential prompts, sensitive internal identifiers, or other private data. <br>
Risk: The skill depends on the external ddgs package and live search services. <br>
Mitigation: Install only from the expected ddgs package source, preferably in a virtual environment, and handle DDGS exceptions or rate limits before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/idkwhodatis/ddgs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include titles, URLs, snippets, source metadata, dates, image links, video links, or book details depending on the selected DDGS method.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
