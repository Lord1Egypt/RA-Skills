## Description: <br>
Automates web and API data extraction with cleaning, formatting, scheduling, proxy support, retries, deduplication, and real-time monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthasking123](https://clawhub.ai/user/arthasking123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data operators use this skill to fetch web pages or API responses and save extracted data for cleaning, formatting, and monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping websites or APIs without authorization, excessive request rates, or improper collection of personal data can create legal, privacy, or service-abuse risk. <br>
Mitigation: Use only sites or APIs you are authorized to access, keep scraping frequency conservative, respect applicable terms and policies, and avoid sensitive personal data unless there is a lawful basis. <br>
Risk: The advertised proxy, retry, and scheduling features are not reliable in the current artifact implementation. <br>
Mitigation: Review and test the script before relying on those features, and replace or fix them for production workflows. <br>
Risk: The script fetches arbitrary URLs with curl and writes raw responses to local files. <br>
Mitigation: Pass trusted URLs, inspect generated files before downstream use, and run the skill in an environment with appropriate filesystem and network controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arthasking123/ai-data-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; runtime output is saved as JSON, HTML, or text files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes scraped content under an output directory using timestamped filenames.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
