## Description:

Automated web task execution service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to propose and run web automation tasks such as scraping, form filling, scheduled checks, API testing, and website monitoring through OpenClaw-style commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound network requests to user-supplied URLs without clear containment.

Mitigation: Run it in a contained network context and add URL allowlisting or private-address blocking before shared or service-style use.

Risk: Web automation can be misused to bypass CAPTCHAs, rate limits, IP bans, or similar security controls.

Mitigation: Refuse bypass requests and direct users to official APIs, written permission, whitelisting, or site-owner coordination.

Risk: Credentials included in URLs, command data, webhooks, or email destinations can leak through logs, shell history, process listings, or referrer headers.

Mitigation: Use environment variables or credential stores, avoid placing secrets in URLs or command arguments, and verify destinations before sending scraped data.

Risk: Bulk extraction of personal data can become unauthorized data harvesting.

Mitigation: Check robots.txt, confirm lawful basis and authorization, and avoid extracting emails, phone numbers, addresses, credentials, or session tokens without verified approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/ai-web-automation-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/ai-web-automation)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown reports and command-oriented guidance with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scrape reports under an output directory when the packaged script is executed.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
