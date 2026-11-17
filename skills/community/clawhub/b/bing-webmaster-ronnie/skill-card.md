## Description:

Bing Webmaster Ronnie helps agents submit URLs to Bing Webmaster Tools and retrieve SEO traffic, keyword, crawl, indexing, and quota data for verified sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ronnine6527](https://clawhub.ai/user/ronnine6527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and SEO teams use this skill to automate Bing URL submissions and generate Bing Webmaster reporting for sites they control. It is suited for scheduled audits, client reporting, and diagnostics that require an existing Bing Webmaster API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Bing Webmaster API key that can access data and submit URLs for verified sites.

Mitigation: Use the BING_WEBMASTER_API_KEY environment variable instead of command-line arguments, limit the key to appropriate sites, avoid logging full request URLs, and rotate any key exposed in shell history or logs.

Risk: Batch or scheduled URL submission can send unintended URLs to Bing if inputs are not reviewed.

Mitigation: Review the site URL and URL list before running submit actions, especially in batch or scheduled workflows, and use the skill only for sites the operator controls.

## Reference(s):

- [Bing Webmaster Tools](https://www.bing.com/webmasters/)
- [ClawHub skill page](https://clawhub.ai/ronnine6527/skills/bing-webmaster-ronnie)
- [Publisher profile](https://clawhub.ai/user/ronnine6527)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal tables, JSON responses, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a BING_WEBMASTER_API_KEY for the relevant verified sites. URL submission performs write actions against Bing Webmaster Tools.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
