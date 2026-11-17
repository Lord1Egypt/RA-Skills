## Description:

Diagnose performance, context, caching, and memory issues in local Ollama calls using LLMxRay’s read-only tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lognebudo](https://clawhub.ai/user/lognebudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local Ollama call performance, prompt context, cache behavior, and video-memory fit, then follow diagnostic recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls routed through the observer may be retained in diagnostic records that contain sensitive prompt content.

Mitigation: Keep the observer local and review recording settings before routing sensitive calls through it.

Risk: The separately downloaded package is not covered by the inspection of the skill instructions.

Mitigation: Use a reviewed, pinned package version consistently for installation and MCP startup.

## Reference(s):

- [LLMxRay project homepage (metadata)](https://github.com/LogneBudo/llmxray)
- [ClawHub skill release page](https://clawhub.ai/lognebudo/skills/diagnose-ollama-calls)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Diagnostic text and recommendations, with Markdown, shell, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic guidance; recommendations are provided for the user to apply.]

## Skill Version(s):

0.8.13 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
