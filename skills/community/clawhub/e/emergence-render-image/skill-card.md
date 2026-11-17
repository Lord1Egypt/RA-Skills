## Description:

Official Emergence Science Skill for rendering professional diagrams (TikZ, Mermaid, Graphviz, D2) via the Emergence Science Render API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Autonomous agents, developers, and engineers use this skill to render structured TikZ, Mermaid, Graphviz, and D2 diagram code into technical visualizations through the Emergence Science Render API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram source and render requests are sent to a hosted third-party Emergence Science API.

Mitigation: Use the skill only when third-party processing is acceptable, and avoid including secrets, private business data, or unreleased proprietary details in submitted diagrams.

Risk: The skill requires a user-provided EMERGENCE_API_KEY.

Mitigation: Store the API key in the agent environment and keep it scoped to the rendering use case described by the skill.

Risk: Heavy LaTeX or diagram rendering can take up to about 1 minute and is subject to account rate limits.

Mitigation: Configure appropriate request timeouts, avoid retry loops, and respect the documented 1-minute per-account rate limit.

Risk: Malicious or unsafe diagram code could violate the provider's governance policy.

Mitigation: Do not submit code intended for sandbox escape, network penetration, or malicious macro injection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emergencescience/skills/emergence-render-image)
- [Emergence Science Web UI](https://emergence.science/)
- [Emergence Science Render API Endpoint](https://api.emergence.science/tools/render)
- [Emergence Science OpenAPI Schema](https://emergence.science/openapi.json)
- [Render Tool OpenAPI Schema](https://api.emergence.science/tools/render/openapi.json)
- [Emergence Science Content Index](https://emergence.science/content/index.json)
- [Bundled Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [API calls, JSON, image files, shell commands, configuration guidance]

**Output Format:** [JSON render responses containing base64 PNG or SVG image data, with optional shell commands for decoding output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EMERGENCE_API_KEY and may take up to about 1 minute for computationally heavy render requests.]

## Skill Version(s):

0.1.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
