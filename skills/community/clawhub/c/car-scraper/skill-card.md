## Description:

Car Scraper collects vehicle listings and details from Dasouche, Dongchedi, and Autohome, then exports the results in OpenClaw-compatible formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackiezhao-eng](https://clawhub.ai/user/jackiezhao-eng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams can use this skill to collect used and new car market data, including listing details, prices, dealer metadata, and vehicle attributes, for downstream OpenClaw workflows. Operators should use it only for data sources and fields they are authorized to collect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a disclosed car-data scraper with anti-bot evasion behavior.

Mitigation: Use it only where collection is permitted, keep request rates conservative, and stop collection when a target site blocks or challenges traffic.

Risk: Outbound network activity may reach unintended domains if configuration or target URLs are changed.

Mitigation: Run the skill in an isolated environment and restrict outbound network access to the intended Dasouche, Dongchedi, and Autohome/Che168 domains.

Risk: Scraped output may contain sensitive fields such as VINs or dealer contact details.

Mitigation: Avoid exporting VINs or dealer contact details unless legally permitted, and treat all JSON, JSONL, and CSV output as untrusted before importing it into agents or opening it in spreadsheets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackiezhao-eng/skills/car-scraper)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Files]

**Output Format:** [Python modules and command-line output that export JSON, JSONL, or CSV vehicle records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw-compatible document records with vehicle metadata such as source platform, price, mileage, VIN when present, dealer fields, images, and timestamps.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
