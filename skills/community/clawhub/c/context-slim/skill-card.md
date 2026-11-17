## Description:

Context Slim profiles prompts, conversations, and system instructions to estimate token use, diagnose context-window pressure, and suggest local compression opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and agent builders use Context Slim to inspect token usage, diagnose truncation risk, and identify compression opportunities before sending or deploying text-only prompts and conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include unescaped content from conversation files.

Mitigation: Open generated reports only from trusted or sanitized inputs until HTML escaping is confirmed fixed.

Risk: The skill analyzes prompts and conversations that may contain sensitive information.

Mitigation: Run it only on files intended for local analysis and choose report output paths deliberately.

Risk: Token counts are heuristic estimates and do not cover multimodal inputs.

Mitigation: Use provider tokenizers for billing or exact context-limit decisions, and add provider-documented costs for images, audio, video, or embedded files.

Risk: Compression recommendations can remove context that is important to the user.

Mitigation: Review suggestions manually before applying them to production prompts or agent instructions.

## Reference(s):

- [Context Slim ClawHub Listing](https://clawhub.ai/theshadowrose/skills/context-slim)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)
- [README](artifact/README.md)
- [Limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; the included tools can emit plain text, JSON, and HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local processing; text-only analysis; token estimates are approximate and compression suggestions require human review.]

## Skill Version(s):

1.0.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
