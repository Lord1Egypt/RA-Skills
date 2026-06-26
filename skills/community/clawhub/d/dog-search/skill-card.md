## Description: <br>
Searches Google through the ScrapingDog API using a bundled Python CLI script that requires SCRAPINGDOG_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent run Google searches through ScrapingDog and present returned result titles, links, snippets, or raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to the third-party ScrapingDog service using the user's SCRAPINGDOG_API_KEY. <br>
Mitigation: Avoid using the skill for secrets, credentials, confidential business content, regulated personal data, or other sensitive search terms. <br>
Risk: The bundled script may need a small bug fix before it runs successfully. <br>
Mitigation: Test the CLI in a controlled environment before relying on it in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/dog-search) <br>
- [ScrapingDog Google API endpoint](https://api.scrapingdog.com/google) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown or plain text search-result summaries, with optional raw JSON output from the bundled CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python, requests, network access to ScrapingDog, and SCRAPINGDOG_API_KEY. The artifact accepts query, country, language, and raw JSON options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
