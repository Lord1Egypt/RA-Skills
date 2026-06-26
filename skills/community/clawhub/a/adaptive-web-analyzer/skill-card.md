## Description: <br>
Fetches webpage or API content, adaptively extracts key text, and uses an LLM to produce structured summaries and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maplee](https://clawhub.ai/user/maplee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve authorized webpage or API content, extract the main text, and generate structured summaries, key points, entity lists, sentiment, and suggested actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch or scrape authenticated and protected web content, including optional stealth behavior. <br>
Mitigation: Use it only on sites and APIs where crawling is authorized, respect robots.txt and rate limits, and avoid stealth or anti-bot modes unless permission is explicit. <br>
Risk: The release requests file.write and system.exec permissions that ClawScan described as unnecessary local command and file access. <br>
Mitigation: Review before installing and remove or restrict file.write and system.exec permissions when the platform allows it. <br>
Risk: Custom headers and authentication inputs could expose sensitive cookies, API tokens, or private system content. <br>
Mitigation: Do not provide credentials for sensitive systems; prefer least-privilege, short-lived tokens and redact sensitive values from prompts and outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maplee/adaptive-web-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/maplee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source URL, fetch time, content statistics, extracted metadata, summary, key points, category, sentiment, entities, suggested actions, and optional raw content preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
