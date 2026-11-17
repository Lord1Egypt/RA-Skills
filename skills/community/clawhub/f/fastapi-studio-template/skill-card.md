## Description:

Bootstrap a dark-themed FastAPI+HTMX studio app with SSE real-time progress, blind test mode, SQLite ratings, and Langfuse tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to bootstrap FastAPI and HTMX studio applications for generative AI comparison, A/B testing, human evaluation, real-time progress streaming, ratings storage, and optional Langfuse tracing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated apps may load HTMX and the SSE extension from third-party browser CDNs.

Mitigation: Vendor browser dependencies locally or add SRI and a restrictive Content Security Policy before deployment.

Risk: Example routes pass prompts in URLs, which can expose prompt content through logs, browser history, or intermediary systems.

Mitigation: Use request bodies for sensitive prompts and avoid storing full prompt text in access logs.

Risk: Langfuse tracing can capture sensitive prompt or output data when enabled.

Mitigation: Make tracing explicit, redact sensitive fields, and set retention limits appropriate for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/fastapi-studio-template)
- [Declared project homepage](https://github.com/reddinft/skill-fastapi-studio-template)
- [HTMX 1.9.12 CDN script](https://unpkg.com/htmx.org@1.9.12)
- [HTMX SSE extension CDN script](https://unpkg.com/htmx.org@1.9.12/dist/ext/sse.js)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python, SQL, HTML, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; optional Langfuse tracing uses LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY when configured.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
