## Description:

Content Orchestrator coordinates content generation, quality gates, scheduling, and publishing across video, image, audio, comic, novel, product, hotspot, upload, and daily operation pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to route content requests into configured pipelines, generate media and product content, apply quality checks, and publish or schedule outputs through connected services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule content to connected accounts.

Mitigation: Require a preview and approval step before every publish or schedule action.

Risk: The skill can run broad local pipelines and helper scripts.

Mitigation: Install it only in environments where local script execution and publishing are explicitly allowed.

Risk: Tenant workflow data may have weak user-facing boundaries.

Mitigation: Lock down writable pipeline and override files, restrict environment-controlled project roots, and avoid sensitive tenant uploads until fallback storage and tenant-filtered listing are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/content-orchestrator)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [business_rules.md](references/business_rules.md)
- [error_codes.md](references/error_codes.md)
- [examples.md](references/examples.md)
- [content_orchestrator_reference.json](scripts/content_orchestrator_reference.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON responses with Markdown guidance and inline command or code examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use configured MCP services, local helper scripts, ffmpeg, and SILICONFLOW_API_KEY-enabled services when installed.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
