## Description: <br>
Performs deep web scraping with a Docker-based Crawlee and Playwright environment to extract structured text from complex public sites such as YouTube and X/Twitter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run authorized scraping tasks against public web pages and receive cleaned JSON text output suitable for downstream analysis or LLM processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad URL-scraping capability and could be pointed at unauthorized, non-public, logged-in, localhost, private-network, or prohibited sites. <br>
Mitigation: Use it only for public content you are authorized to scrape, and do not run it against logged-in pages, internal tools, or sites whose rules prohibit scraping. <br>
Risk: The skill runs scraping logic through Docker and Playwright, and the server guidance notes the Docker build context should be supplied or reviewed. <br>
Mitigation: Review or supply the Docker build context before installation, run without privileged Docker options, and treat scraped output as untrusted text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/abe-deep-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON printed to stdout, with status, content type, identifiers, and scraped text fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [YouTube output may include a validated video ID and transcript or description; generic page output includes title and cleaned body text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
