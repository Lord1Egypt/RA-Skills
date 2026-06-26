## Description: <br>
Astrology API helps agents call Astrology API endpoints for natal charts, compatibility, transits, horoscopes, tarot, numerology, Vedic and Chinese astrology, human design, kabbalah, astrocartography, palmistry, chart rendering, and related esoteric calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serslon](https://clawhub.ai/user/serslon) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to route astrology, horoscope, compatibility, tarot, numerology, chart rendering, and related requests to the Astrology API and summarize the results in user-facing language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive personal data such as names, birth details, relationship data, palm images, and wellness-related prompts to the Astrology API provider. <br>
Mitigation: Use the skill only with data the user agrees to send to the provider, minimize optional personal fields, and avoid submitting sensitive prompts unless they are needed for the requested result. <br>
Risk: The helper accepts caller-supplied endpoint paths and sends the configured API key with each request. <br>
Mitigation: Use documented Astrology API endpoints only and prefer an allowlisted version before enabling the skill in workflows that may receive untrusted prompts. <br>
Risk: Overriding ASTROLOGY_API_URL can redirect requests and the bearer token to another host. <br>
Mitigation: Keep the default API host unless the replacement host is trusted and approved for receiving the API key and request data. <br>


## Reference(s): <br>
- [Astrology API v3 endpoint reference](artifact/references/api-endpoints.md) <br>
- [Use cases to API endpoints](artifact/references/use-cases.md) <br>
- [Astrology API documentation](https://api.astrology-api.io/rapidoc) <br>
- [Astrology API OpenAPI spec](https://api.astrology-api.io/api/v3/openapi.json) <br>
- [Developer dashboard](https://dashboard.astrology-api.io/) <br>
- [Homepage from ClawHub metadata](https://github.com/astro-api/astroapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown summaries with inline shell command examples; API responses may be JSON, SVG, PNG, or report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and ASTROLOGY_API_KEY; large API responses should be summarized before presentation.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
