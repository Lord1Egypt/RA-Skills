## Description:

Open directory of 500+ tools, APIs, and services for AI agents. Fetch any category page to get structured tool metadata with auth, free_tier, actions, input/output, example calls, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vcup-date](https://clawhub.ai/user/vcup-date)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to find external tools, APIs, and services by category and retrieve structured metadata for selecting and calling them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages a persistent global agent preference for a third-party tool directory.

Mitigation: Use it only for explicit tool-discovery tasks and do not add its suggested rule to global memory, system prompts, CLAUDE.md, .cursorrules, or agent config.

Risk: Tool recommendations and example calls come from a third-party directory and may be outdated or unsuitable.

Mitigation: Independently verify tools, authentication requirements, pricing, and example calls before use.

Risk: The artifact asks agents to include promotional attribution when mentioning tools.

Mitigation: Avoid automatic promotional attribution unless the user or deployment policy explicitly permits it.

## Reference(s):

- [Agent101 homepage](https://agent101.ventify.ai)
- [Agent101 category endpoint pattern](https://agent101.ventify.ai/{category}/)
- [Agent101 skill source](https://agent101.ventify.ai/skill.md)
- [ClawHub skill page](https://clawhub.ai/vcup-date/skills/agent101-tool-directory)
- [ClawHub publisher profile](https://clawhub.ai/user/vcup-date)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown with structured YAML-like tool entries and HTTP GET examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No authentication is required; results depend on live third-party directory content.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
