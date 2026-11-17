## Description:

AI-powered professional networking assistant. Generate personalized cold emails and outreach playbooks to accelerate career growth and business development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hotwheelsbo](https://clawhub.ai/user/hotwheelsbo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate personalized professional outreach, including cold email drafts and outreach playbooks, from a user's LinkedIn profile, a target contact's LinkedIn profile, and a stated objective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends email addresses, verification codes, LinkedIn profile URLs, target LinkedIn URLs, and outreach objectives to Articuler.

Mitigation: Ask users to confirm they are comfortable sharing that information with Articuler, and avoid submitting sensitive contacts or regulated business information unless the provider's data handling is acceptable.

Risk: The login flow returns a token required for later API calls.

Mitigation: Treat the token as a secret, avoid displaying it unnecessarily, and do not store it longer than needed for the current workflow.

Risk: Generated outreach may be incorrect, overstate facts, or feel inappropriate for the target contact.

Mitigation: Present cold emails and playbooks for user review and editing before any message is sent or acted on.

## Reference(s):

- [Articuler](https://www.articuler.ai)
- [Articuler MCP endpoint](https://www.articuler.ai/mcp)
- [ClawHub skill page](https://clawhub.ai/hotwheelsbo/skills/articuler)
- [Publisher profile](https://clawhub.ai/user/hotwheelsbo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with API request examples and generated outreach content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft cold emails and structured outreach playbooks; requires user review before any outreach is sent.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
