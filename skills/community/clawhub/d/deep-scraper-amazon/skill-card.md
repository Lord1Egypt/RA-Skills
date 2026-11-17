## Description:

Deep Scraper + Amazon is a Dockerized Crawlee and Playwright web-scraping skill for Amazon product data, YouTube transcripts, and general dynamic web-page text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiafar](https://clawhub.ai/user/jiafar)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to run containerized browser scraping workflows for Amazon market research, product-detail extraction, YouTube transcript capture, and generic public web-page text extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse arbitrary third-party URLs and return retrieved content without sufficient safeguards against unintended internal or private targets.

Mitigation: Use explicit public URLs only, avoid authenticated, private, and internal targets, and block container access to local networks and metadata services.

Risk: The Dockerized browser scraper may expose sensitive page content in command output if used against non-public pages.

Mitigation: Review targets before execution, avoid pages containing credentials or private data, and inspect returned content before sharing it.

Risk: The skill depends on a container image and JavaScript browser automation dependencies whose provenance may not be independently established by the server evidence.

Mitigation: Rebuild from reviewed source, pin and review dependencies, and verify image provenance before use in sensitive environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiafar/skills/deep-scraper-amazon)
- [Publisher profile](https://clawhub.ai/user/jiafar)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scraper commands return JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generic page output is capped at 10000 characters; YouTube transcript output is capped at 15000 characters; Amazon handlers return structured product fields such as ASIN, price, rating, reviews, rank, image URL, and boughtPastMonth when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
