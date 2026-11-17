## Description:

Provides AI impact scores, 2030 forecasts, salary context, career advice, and AI tool suggestions for 103 Dutch CBS BRC 2014 occupation groups through a public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simondjanssen](https://clawhub.ai/user/simondjanssen)

### License/Terms of Use:

MIT-0

## Use Case:

Dutch-speaking workers, career advisors, analysts, and agents use this skill to look up occupation-level AI exposure, labor-market forecasts, salary context, and practical AI tools for Dutch CBS BRC 2014 occupation groups.

### Deployment Geography for Use:

Netherlands

## Known Risks and Mitigations:

Risk: The skill contacts simondjanssen.nl for occupation lookups.

Mitigation: Review network access expectations before installation and use it only where calls to this public API are acceptable.

Risk: The occupational AI scores, forecasts, salary context, and career advice are estimates and may be incomplete or outdated.

Mitigation: Treat outputs as informational guidance and compare them with current labor-market, employer, and professional sources before making career or workforce decisions.

Risk: Fuzzy occupation matching can return an adjacent occupation group rather than the user's exact role.

Mitigation: Check the returned occupation name and sector before relying on the score, forecast, salary, or tool suggestions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simondjanssen/skills/ai-bloodstellingskaart)
- [AI Blootstellingskaart](https://simondjanssen.nl/ai-kaart)
- [Methodologie](https://simondjanssen.nl/ai-kaart/methodologie)
- [Beroep API](https://simondjanssen.nl/api/beroep)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown summaries with optional JSON API response excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public API lookup URLs for occupation queries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
