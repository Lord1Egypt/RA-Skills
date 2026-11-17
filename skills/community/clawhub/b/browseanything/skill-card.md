## Description:

BrowseAnything delegates live web tasks to a hosted Chromium browser agent that can browse sites, fill forms, extract data, and return results with screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehdi149](https://clawhub.ai/user/mehdi149)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and skill-aware agents use this skill to delegate live web workflows such as research, form completion, authenticated data extraction, screenshots, monitoring, and shopping tasks to BrowseAnything's hosted browser automation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act in logged-in browser sessions, submit forms or transactions, and export private data.

Mitigation: Require explicit user review before logins, form submissions, purchases, bookings, or private data exports.

Risk: Browser prompts and page contents may send sensitive browsing data to a remote BrowseAnything service.

Mitigation: Install only when the BrowseAnything service is trusted, prefer project-scoped installation, and use limited, revocable API keys.

Risk: Human-in-the-loop prompts may request 2FA codes, secrets, or other sensitive values.

Mitigation: Avoid passing 2FA codes or secrets as command-line arguments; ask the user directly and use safer input handling when sensitive values are required.

Risk: Custom BrowseAnything endpoints can redirect browser automation traffic outside the hosted platform.

Mitigation: Keep custom endpoints HTTPS-only and verify the endpoint owner before using BROWSEANYTHING_API_URL.

## Reference(s):

- [BrowseAnything homepage](https://browseanything.io)
- [BrowseAnything platform docs](https://platform.browseanything.io/docs)
- [ClawHub skill page](https://clawhub.ai/mehdi149/skills/browseanything)
- [Browse Anything API Reference](REFERENCE.md)
- [Browse Anything prompt patterns](EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, files]

**Output Format:** [Plain text or JSON task results, Markdown tables when requested, and PNG screenshot files from the screenshot helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BROWSEANYTHING_API_KEY; tasks may pause for human input and are subject to tier-dependent step, time, rate, and concurrency limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
