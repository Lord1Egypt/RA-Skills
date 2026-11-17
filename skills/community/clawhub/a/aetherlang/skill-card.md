## Description:

Execute AI workflow orchestration flows using the AetherLang Omega DSL for multi-step AI pipelines across recipes, business strategy, market analysis, molecular gastronomy, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[contrario](https://clawhub.ai/user/contrario)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit AetherLang flow DSL and explicit query text to an external API that executes AI workflow orchestration flows and returns structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flow DSL and query text are transmitted to an external service at api.neurodoc.app.

Mitigation: Inform users before the first API call and send only the explicit flow code and query text needed for the request.

Risk: Prompts may accidentally include secrets, credentials, personal data, private files, or confidential business information.

Mitigation: Strip sensitive content before sending requests and ask the user to provide a sanitized query when needed.

Risk: Generated workflow outputs may be incomplete, incorrect, or unsuitable for high-impact decisions without review.

Mitigation: Have a qualified person review API results before using them for business, culinary safety, scientific, medical, legal, or financial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/contrario/skills/aetherlang)
- [AetherLang Homepage](https://masterswarm.net)
- [AetherLang Execute API Endpoint](https://api.neurodoc.app/aetherlang/execute)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Guidance]

**Output Format:** [Markdown and JSON-like structured response text from an external API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends only explicit flow DSL code and query text to api.neurodoc.app; no credentials are required.]

## Skill Version(s):

9.9.11 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
