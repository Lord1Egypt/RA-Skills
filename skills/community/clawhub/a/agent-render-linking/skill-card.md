## Description:

Creates zero-retention agent-render.com links for markdown, code, diffs, CSV, or JSON artifacts so agents can share browser-rendered artifacts instead of raw chat content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baanish](https://clawhub.ai/user/baanish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to package markdown, code, diffs, CSV, or JSON artifacts into agent-render.com links for browser review across chat platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated links can expose private artifacts to anyone who receives the URL.

Mitigation: Do not use the skill for secrets, credentials, confidential code, private customer data, or other sensitive content unless sharing the URL is intentional; use a self-hosted viewer or confirm before generating links for sensitive workflows.

Risk: Large artifacts can exceed practical URL or chat-platform budgets.

Mitigation: Use the shortest supported codec, packed wire mode, and focused artifacts; return a clear budget failure instead of silently truncating content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baanish/skills/agent-render-linking)
- [Agent Render public viewer](https://agent-render.com)
- [Agent Render ARX dictionary](https://agent-render.com/arx-dictionary.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or platform-specific linked text containing agent-render.com URLs and concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payload content remains in URL fragments; raw URLs are used when linked text is not reliable for the target chat surface.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
