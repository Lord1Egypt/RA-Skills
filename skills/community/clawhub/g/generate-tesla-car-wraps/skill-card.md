## Description:

Call Craftsman Agent API OneKey Router to generate Tesla car wrap images and paint visualizations for display on a 3D screen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative workflow users use this skill to request Tesla wrap concepts through a routed image-generation API, with CLI, Python, and TypeScript examples for integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference image URLs are sent to an external routed API and could expose sensitive creative inputs or private image links.

Mitigation: Use only non-sensitive prompts and public or intentionally shared reference image URLs.

Risk: The documented installation paths include global, unpinned dependencies that can expand install-scope risk.

Mitigation: Prefer pinned versions in a local or isolated environment before deployment.

Risk: The skill requires an API key and sends it as an authentication header.

Mitigation: Set the API key deliberately through the environment, restrict who can access it, and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/generate-tesla-car-wraps)
- [DeepNLP Workspace keys](https://www.deepnlp.org/workspace/keys)
- [OneKey router endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated image URLs from the routed API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
