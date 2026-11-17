## Description:

Converts natural-language descriptions or Mermaid code into flowchart images, with optional DeepSeek or OpenAI generation, Mermaid templates, multiple diagram types, and troubleshooting support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andapeng](https://clawhub.ai/user/andapeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other technical users can generate Mermaid-based workflow, sequence, Gantt, class, state, pie, journey, and timeline diagrams from plain-language prompts or raw Mermaid syntax. The skill is suited to documentation, architecture planning, business process mapping, and quick diagram prototyping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram prompts may be sent to DeepSeek, OpenAI, or a configured custom endpoint.

Mitigation: Use --no-llm, --use-template, or --raw for private diagrams, and only enable remote providers for content approved for external processing.

Risk: Stored or command-line API credentials may be used by the skill.

Mitigation: Prefer narrowly scoped environment variables or protected OpenClaw configuration, avoid passing live keys with --api-key, and rotate any exposed credentials.

Risk: The installer uses global npm and pip dependency installation that may be unpinned.

Mitigation: Review dependencies before installation, use an isolated environment where possible, and avoid sudo unless system-wide installation risk is accepted.

Risk: Custom base URLs can direct prompts and credentials to untrusted services.

Mitigation: Use custom endpoints only after verifying the operator, transport security, and data handling policy.

## Reference(s):

- [Flowchart Gen on ClawHub](https://clawhub.ai/andapeng/skills/flowchart-gen)
- [Publisher profile: andapeng](https://clawhub.ai/user/andapeng)
- [Mermaid syntax guide](references/syntax-guide.md)
- [Mermaid documentation](https://mermaid.js.org/)
- [Mermaid flowchart syntax](https://mermaid.js.org/syntax/flowchart.html)
- [Mermaid live editor](https://mermaid.live/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus generated Mermaid code and PNG, SVG, or PDF diagram files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run without LLM calls using --no-llm, --use-template, or --raw; image rendering depends on Mermaid CLI and local environment setup.]

## Skill Version(s):

1.1.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
