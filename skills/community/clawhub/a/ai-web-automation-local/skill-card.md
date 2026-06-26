## Description: <br>
Fetches a target webpage and writes a Markdown scraping report with HTTP status, content length, page title, and link count. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larry-at](https://clawhub.ai/user/larry-at) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to collect basic status and metadata from webpages they are authorized to access. The implemented artifact is best suited for simple scraping reports rather than full browser automation, scheduling, proxy-pool operation, or notification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises form filling, scheduling, proxy pools, Selenium/Puppeteer, testing, and notifications that are not present in the artifact implementation. <br>
Mitigation: Treat the release as a basic webpage scraper until the publisher adds matching implementation and safety guidance. <br>
Risk: Scraping arbitrary URLs can violate site terms, privacy expectations, or authorization boundaries. <br>
Mitigation: Verify target URLs before use and scrape only sites the operator is authorized to access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/larry-at/ai-web-automation-local) <br>
- [Publisher profile](https://clawhub.ai/user/larry-at) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report written to a local output file, with a console message containing the saved path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided action and URL; the implemented action is scrape.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
