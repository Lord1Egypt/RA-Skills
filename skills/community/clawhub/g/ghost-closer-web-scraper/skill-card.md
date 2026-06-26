## Description: <br>
Scrape complete business intelligence from Google Maps, Facebook, and Instagram for any local business, returning structured JSON with ratings, contact info, services, and media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamsarts](https://clawhub.ai/user/dreamsarts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business teams use this skill to collect structured local-business profiles for lead generation, page building, and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a live Chrome session, which can expose existing browser state if run in a personal profile. <br>
Mitigation: Run it only in an isolated browser profile with no personal logins before collecting data. <br>
Risk: The artifact loads a hard-coded local .env path. <br>
Mitigation: Inspect or remove the hard-coded .env loading and provide only the configuration needed for the run. <br>
Risk: The scraper contacts Google Maps, Facebook, Instagram, and discovered business websites. <br>
Mitigation: Confirm the domains and collection activity are appropriate for the intended use before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dreamsarts/ghost-closer-web-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Code] <br>
**Output Format:** [Structured JSON printed to stdout, with operational messages and errors written to stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fields may be null when a source has no result or cannot be reached.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
