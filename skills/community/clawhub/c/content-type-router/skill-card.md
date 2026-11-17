## Description:

Detect and route to the correct visual content type (hero shot, poster, infographic, etc.) from a text description or output type hint. Use when you need to classify a content generation request into a structured type with layout rules, visual mode, and generation hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-generation agents use this skill to classify visual content requests into structured content types with layout, typography, visual mode, and generation-prompt hints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional database-backed content type rules can influence downstream image prompts if enabled or misconfigured.

Mitigation: Keep database mode disabled unless it is required; when enabling it, review the Supabase table contents, credentials, and rule changes before use.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [Content Type Router on ClawHub](https://clawhub.ai/phy041/skills/content-type-router)
- [Publisher Profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured content type descriptions and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes content type slugs, confidence guidance, layout rules, visual modes, generation hints, and optional database-mode configuration guidance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
