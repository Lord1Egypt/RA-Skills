## Description: <br>
Scrape any web page with a headless browser and extract text or screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the GetPost web scraping API for page text extraction, screenshots, and selector-based waits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the external service endpoint is ambiguous. <br>
Mitigation: Verify who currently controls getpost.dev before installing or using the skill. <br>
Risk: Scraping can send URLs and scraped content to a third-party service. <br>
Mitigation: Use only pages you are allowed to scrape and avoid private, regulated, or sensitive content. <br>
Risk: The skill uses a bearer key for the GetPost API. <br>
Mitigation: Store the GetPost bearer key securely and do not expose it in prompts, logs, or shared files. <br>


## Reference(s): <br>
- [GetPost scrape API reference](https://getpost.dev/docs/api-reference#scrape) <br>
- [ClawHub skill page](https://clawhub.ai/dommholland/getpost-scrape) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage instructions for authentication and scrape requests; the external service may return extracted text or screenshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
