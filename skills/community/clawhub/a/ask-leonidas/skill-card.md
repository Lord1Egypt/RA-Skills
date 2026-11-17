## Description:

Generate a structured LEONIDAS prompt from any professional pain point using the Ask Leonidas OpenClaw API, with automatic role, industry, and desired outcome inference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonidas-esquire](https://clawhub.ai/user/leonidas-esquire)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn business or workflow pain points into structured prompts for SOUL.md, AGENTS.md, cron job instructions, skill briefs, and agent-owned workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send API keys and prompt-related business context to the API base URL configured in the environment.

Mitigation: Set ASK_LEONIDAS_API_BASE exactly to https://askleonidas.com and avoid entering secrets, customer data, regulated data, or highly confidential details in pain points.

Risk: On API failure, the skill may open the configured service URL in a browser fallback.

Mitigation: Review browser fallback behavior before deployment and prefer a version that validates the API host and asks before opening a browser.

## Reference(s):

- [Ask Leonidas homepage](https://askleonidas.com)
- [Ask Leonidas ClawHub skill page](https://clawhub.ai/leonidas-esquire/skills/ask-leonidas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-formatted metadata followed by generated prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detected role, detected industry, detected desired outcome, confidence, quality score, prompt type, and request ID when returned by the service.]

## Skill Version(s):

2.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
