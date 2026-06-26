## Description: <br>
Searches Douyin video content from natural-language requests using browser automation and returns titles, authors, engagement metrics, and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to issue natural-language Douyin search requests and receive scraped video result summaries through browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-activation may trigger browser-based Douyin searches from vague topic prompts. <br>
Mitigation: Invoke the skill only with explicit Douyin search wording and review the intended search terms before execution. <br>
Risk: Saved browser state can include Douyin login credentials or session tokens. <br>
Mitigation: Treat any saved douyin-auth.json file like a password: keep it out of source control, do not share it, and delete it when no longer needed. <br>
Risk: Browser scraping can expose sensitive search terms and may encounter platform access limits or verification flows. <br>
Mitigation: Avoid sensitive search terms and expect manual review when Douyin prompts for login, verification, or rate-limit handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-scraper-openclaw) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Natural-language search examples](artifact/examples/search_requests.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summaries with inline shell commands when executing browser automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include Douyin video titles, author names, engagement metrics, links, and saved browser-session guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
