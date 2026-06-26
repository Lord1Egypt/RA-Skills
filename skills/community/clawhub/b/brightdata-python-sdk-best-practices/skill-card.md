## Description: <br>
Guide for writing, modifying, debugging, or reviewing Python code that uses the Bright Data SDK for scraping, search, datasets, Bright Data APIs, or browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to write, modify, debug, and review Python code that uses Bright Data SDK features for web scraping, search results, datasets, Scraper Studio, and browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Bright Data examples can initiate scraping, search, dataset export, browser automation, or zone-management workflows that may have authorization, privacy, or billing impact. <br>
Mitigation: Review the target site or dataset authorization, billing implications, and account settings before running generated code; require explicit user confirmation for zone creation, zone deletion, dataset exports, and browser automation. <br>
Risk: Generated examples may need Bright Data API tokens or Browser API credentials. <br>
Mitigation: Load credentials from environment variables or a local secret manager and keep them out of source code, prompts, logs, and committed files. <br>


## Reference(s): <br>
- [Bright Data Python SDK - Full API Reference](references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/meirk-brd/brightdata-python-sdk-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated examples may reference Bright Data API tokens, Browser API credentials, paid scraping operations, dataset exports, and zone-management actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
