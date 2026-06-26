## Description: <br>
Dataify Google Shopping turns shopping search, product search, and price comparison requests into confirmed Dataify Scraper API calls for Google Shopping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare, confirm, and run Google Shopping product searches through Dataify's Scraper API, including locale, price, shipping, sale, pagination, and output-format parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries, locale settings, and filters are sent to the Dataify Scraper API for Google Shopping requests. <br>
Mitigation: Use the skill only when that integration is intended, avoid private purchase plans in queries, and review the confirmation table before approving a call. <br>
Risk: Live calls require a Dataify API token or a user-provided token. <br>
Mitigation: Provide tokens only through the expected token handling path, confirm the destination before use, and never display the token in parameter previews or final answers. <br>


## Reference(s): <br>
- [Dataify Google Shopping API Reference](references/google_shopping_api.md) <br>
- [ClawHub release page](https://clawhub.ai/dataify-server/dataify-google-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown parameter tables, shell command invocations, and raw API response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before live API calls and masks tokens in previews.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
