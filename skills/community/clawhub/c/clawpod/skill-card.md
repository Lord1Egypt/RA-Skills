## Description:

Read any website or search Google, even when sites block bots or are geo-restricted. Handles CAPTCHAs, JavaScript rendering, and anti-bot protection server-side via residential proxies. Returns HTML or structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and agents use Clawpod to retrieve rendered web pages and Google search results when ordinary fetching is blocked, incomplete, or requires localization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad HTTPS curl authority and can send target URLs or search queries to an external unblocker service.

Mitigation: Review commands before execution, use only the documented Massive Unblocker endpoints, and avoid secrets, internal-only URLs, regulated data, or sensitive personal queries.

Risk: The skill is designed for anti-bot, CAPTCHA, geo-restriction, and paywall-related fetching workflows.

Mitigation: Use it only for URLs and searches the user is authorized to send to the service, and confirm legal or policy constraints before using it on restricted content.

## Reference(s):

- [ClawPod homepage](https://clawpod.joinmassive.com)
- [ClawHub skill page](https://clawhub.ai/codeninja23/skills/clawpod)
- [OpenClaw skill definition](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash examples; API responses are rendered HTML text or structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and MASSIVE_UNBLOCKER_TOKEN; target URLs and search terms are sent to Massive's Unblocker service.]

## Skill Version(s):

0.1.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
