## Description: <br>
Fetch web pages and extract readable content for AI use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aurthes](https://clawhub.ai/user/Aurthes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve, summarize, or extract structured information from public web pages and small URL sets with fallbacks for blocked or JavaScript-heavy pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs and page contents may be sent to third-party readability services. <br>
Mitigation: Use the skill for public pages or URLs that are acceptable to share with those services, and avoid private documents, presigned links, intranet or localhost URLs, account pages, and sensitive query parameters. <br>
Risk: Direct fetches can return challenge pages, login walls, or thin content instead of the requested page. <br>
Mitigation: Treat blocked or thin responses as unreliable and use browser or search-based fallback methods with confidence notes. <br>


## Reference(s): <br>
- [Web Fetcher on ClawHub](https://clawhub.ai/Aurthes/aurthes-web-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON fetch results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch attempts report the selected method, attempt history, blocked or thin-content detection, and final content when successful.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
