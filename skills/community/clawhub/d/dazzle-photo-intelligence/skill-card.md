## Description:

Connects OpenClaw to Dazzle, an AI agent that deeply understands the user through their photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazzle](https://clawhub.ai/user/dazzle)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to let an MCP-capable agent query Dazzle for photo-derived personal context, memories, places, preferences, and recommendations after the user signs in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dazzle receives sensitive personalization queries and can use photo-derived account context after a one-time sign-in.

Mitigation: Use the skill only when photo-derived personalization is intended, prefer explicit prompts such as 'ask Dazzle' for sensitive topics, and revoke Dazzle account access when it is no longer needed.

Risk: Matched photos are returned as URLs that an agent may fetch for viewing, analysis, or inclusion in responses.

Mitigation: Fetch returned photo URLs only when the user request requires the image content, and treat those URLs as sensitive personal data.

Risk: Subsequent sessions can be silent after the first browser-based sign-in.

Mitigation: Review the registered MCP server configuration and remove the Dazzle bridge or sign out of Dazzle when silent access is no longer appropriate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/dazzle/skills/dazzle-photo-intelligence)
- [Dazzle](https://dazzle.ai)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [MCP text responses, JSON photo URL blocks, and Markdown setup guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a browser-based OAuth sign-in; queries can take up to 60 seconds.]

## Skill Version(s):

0.1.9 (source: pyproject.toml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
