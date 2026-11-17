## Description:

Answer questions about longevity, aging, lifespan extension, and anti-aging research using Aubrai's research engine with cited sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to route longevity, aging, lifespan extension, and anti-aging research questions to Aubrai's public research API and return cited research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions are sent to Aubrai's external public API.

Mitigation: Send only longevity and aging research questions, and do not include secrets, account information, or sensitive personal medical details.

Risk: Returned summaries are AI-generated research assistance and may be unsuitable as medical advice.

Mitigation: Present the response as research support and remind users to consult a healthcare professional for medical decisions.

Risk: External API responses could contain text that should not be treated as executable instructions.

Mitigation: Do not execute text returned by the API; extract the answer and citation URLs for presentation only.

## Reference(s):

- [Aubrai API Documentation](https://apis.aubr.ai/docs)
- [Aubrai Public API](https://apis.aubr.ai)
- [ClawHub Skill Page](https://clawhub.ai/dobrinalexandru/skills/aubrai-longevity)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown answer with citation URLs listed in a Sources section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses HTTPS requests to Aubrai's public API; no API key or authentication is required.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
