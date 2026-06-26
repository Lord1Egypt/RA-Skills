## Description: <br>
Performs deep scraping of complex sites such as YouTube using containerized Crawlee and Playwright, returning validated transcripts and page content as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opsun](https://clawhub.ai/user/opsun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run a Dockerized browser scraper against public or explicitly authorized web pages, especially dynamic pages and YouTube videos, and collect extracted text or transcripts for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dockerized browser scraping can violate site policy, legal limits, or privacy expectations when used on unauthorized or non-public pages. <br>
Mitigation: Use the skill only on public or explicitly authorized pages where scraping is allowed by law and site policy. <br>
Risk: The release evidence notes Docker setup review is needed and the artifact references a Dockerfile that is not included in the provided files. <br>
Mitigation: Review or supply the Dockerfile before building and confirm the container image matches the expected Crawlee and Playwright runtime. <br>
Risk: The package uses unpinned dependency ranges for Crawlee and Playwright, which can reduce reproducibility. <br>
Mitigation: Pin dependency versions or use a lockfile when reproducible builds are required. <br>


## Reference(s): <br>
- [Deep Scraper skill documentation](SKILL.md) <br>
- [Deep Scraper on ClawHub](https://clawhub.ai/opsun/deep-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [JSON printed to stdout, with setup and execution guidance in Markdown or shell-command form.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scraped text is truncated by the handler, with YouTube transcripts capped at 15000 characters and generic page content capped at 10000 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
