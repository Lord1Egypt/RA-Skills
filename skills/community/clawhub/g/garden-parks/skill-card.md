## Description:

Explore classical Chinese gardens, city parks, botanical gardens, and royal gardens, with FlyAI/Fliggy-backed travel search and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search garden, park, botanical garden, and attraction options through FlyAI CLI output, then present concise Markdown results with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install and invoke an unpinned third-party global npm CLI.

Mitigation: Use a pinned and reviewed @fly-ai/flyai-cli version, and require explicit approval before installing or invoking external tools.

Risk: Garden and park searches are routed through FlyAI/Fliggy and may return commercial booking links.

Mitigation: Use the skill only when provider routing and booking links are acceptable, and clearly preserve the provider booking-link context in outputs.

Risk: The artifact describes local plaintext logging of raw user queries.

Mitigation: Disable or remove persistent raw-query logging, or redact sensitive query content before any local persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/garden-parks)
- [Templates reference](references/templates.md)
- [Playbooks reference](references/playbooks.md)
- [Fallbacks reference](references/fallbacks.md)
- [Runbook reference](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries, comparison tables, booking links, and inline shell commands for setup or retry guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should be based on FlyAI CLI output and include provider booking links when results are shown.]

## Skill Version(s):

v3.2.2 (source: server release metadata; artifact frontmatter reports 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
