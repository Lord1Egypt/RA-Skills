## Description:

Discover and scrape public Facebook pages and groups by location and category with browser simulation and export data in JSON or CSV formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arulmozhiv](https://clawhub.ai/user/arulmozhiv)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to discover and scrape public Facebook pages and groups by location, category, or page name, then export structured data for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for Facebook scraping and may be used on data the operator is not authorized to collect.

Mitigation: Use only for data the operator is authorized to collect and review planned collection against applicable platform, legal, and organizational requirements before running it.

Risk: Proxy, browser simulation, and anti-detection guidance could be used to bypass rate limits, account blocks, or IP blocks.

Mitigation: Do not use the skill to bypass Facebook limits or blocks; define conservative quotas and stop collection when rate limiting or blocking signals appear.

Risk: Collected contact details, page metadata, post engagement, and downloaded images may create privacy and retention risk.

Mitigation: Minimize stored fields, restrict access to outputs, and define deletion rules for contact data, images, queue files, and exports.

Risk: Proxy and API credentials are required for some workflows and could be exposed through configuration or logs.

Mitigation: Store proxy and API credentials as secrets, avoid committing configuration with secrets, and review logs for accidental credential disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arulmozhiv/skills/facebook-scraper)
- [ScrapeClaw](https://www.scrapeclaw.cc/)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Programmable Search Engine](https://programmablesearchengine.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described scraper exports JSON, CSV, and thumbnail files.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
