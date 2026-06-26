## Description: <br>
Fetches public web pages and extracts readable content for AI reading, summarization, and small-scale crawling with fallback retrieval methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aurthes](https://clawhub.ai/user/Aurthes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to fetch article or page text and extract structured fields from public URLs. It helps agents switch between direct markdown conversion, browser inspection, and search-based fallback when a site blocks direct retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive URLs or confidential pages may be sent to named web conversion services during direct fetch attempts. <br>
Mitigation: Use the skill for public pages by default; avoid intranet links, signed links, password-reset URLs, token-bearing URLs, and confidential pages unless sharing them with those services is intentional. <br>
Risk: Browser fallback can expose the contents of an attached live page to the agent. <br>
Mitigation: Attach browser tabs only when the user intentionally wants the agent to inspect that page, and extract only the fields needed for the task. <br>
Risk: Blocked or protected sites can return challenge, login, or thin-content pages instead of the target content. <br>
Mitigation: Treat block markers and incomplete content as retrieval failures, then use browser or search fallback and label any secondary-source results clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Aurthes/aurthes-web-fetcher-v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and JSON fetch results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include extraction method, confidence, and notes for blocked or unresolved rows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
