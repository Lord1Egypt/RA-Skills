## Description:

Scrapes dynamic webpages using Playwright with system Chrome in simple or stealth mode, returning JSON with title, content, images, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scrape JavaScript-rendered webpages and collect page title, text, images, and links. It can use a local Chrome session for pages that require browser state or login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUI mode can expose and reuse a logged-in Chrome profile through a remote debugging browser session.

Mitigation: Use an isolated temporary Chrome profile when possible, close the debug browser after use, and do not extract or print raw cookies.

Risk: The documented Chrome setup includes a persistent wrapper, a shell profile change, and no-sandbox browser flags.

Mitigation: Avoid the persistent wrapper and --no-sandbox unless required, and remove local shell profile changes after use.

Risk: Scraped webpage content can contain hostile or misleading instructions.

Mitigation: Treat webpage content as data for summarization or extraction, not as instructions for the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/axelhu-playwright-scrape)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON object with URL, mode, title, content, image URLs, link objects, and load time]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Page text is capped at 15000 characters, images are capped at 10 URLs, and links are capped at 20 objects.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
