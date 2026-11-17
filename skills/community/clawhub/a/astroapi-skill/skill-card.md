## Description:

Astrology API helps agents call a third-party astrology API to generate astrological charts, horoscopes, compatibility readings, tarot and numerology outputs, and related reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serslon](https://clawhub.ai/user/serslon)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to answer astrology, horoscope, compatibility, tarot, numerology, and related esoteric requests by collecting the needed inputs, calling Astrology API endpoints, and summarizing results in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive personal data may be sent to a third-party astrology API, including precise birth details, relationship data, sensitive question topics, and palm images.

Mitigation: Share only data the user is comfortable sending; avoid unnecessary names, emails, free-form notes, and images.

Risk: The ASTROLOGY_API_URL override can redirect requests and expose the API key and request data to another destination.

Mitigation: Leave ASTROLOGY_API_URL unset unless the destination is explicitly trusted and expected.

Risk: The server security verdict is suspicious because data sharing is under-disclosed and the URL override can change where requests are sent.

Mitigation: Review the skill before installation and execution, especially before using real personal data.

## Reference(s):

- [API Endpoint Reference](references/api-endpoints.md)
- [Use Cases to API Endpoints](references/use-cases.md)
- [Astrology API Documentation](https://api.astrology-api.io/rapidoc)
- [Astrology API](https://api.astrology-api.io/)
- [Astrology API Skill Homepage](https://github.com/astro-api/astroapi-skill)
- [Astrology API Developer Dashboard](https://dashboard.astrology-api.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown summaries, JSON API responses, shell command snippets, and optional SVG, PNG, JPG, WebP, or PDF chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and ASTROLOGY_API_KEY; chart rendering requests may save image files for the user.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
