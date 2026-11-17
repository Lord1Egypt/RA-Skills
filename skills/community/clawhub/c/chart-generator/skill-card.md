## Description:

Chart Generator helps agents create styled chart images from structured data through AgentPMT-hosted remote chart-generation calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate bar, line, pie, scatter, doughnut, radar, bubble, polar area, and horizontal bar charts for reports, dashboards, presentations, publications, email, and social media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart inputs and generated images may be sent to AgentPMT and QuickChart-compatible remote processing.

Mitigation: Send only data appropriate for remote processing; for confidential, regulated, or proprietary data, prefer return_base64=true with store_file=false when possible.

Risk: Stored chart files are available through signed URLs until they expire.

Mitigation: Disable storage when a URL is not needed, or set the shortest supported expiration_days value.

Risk: Setup snippets include package-install commands that may change over time if left unpinned.

Mitigation: Verify the package source and version before running npx-based setup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/chart-generator)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/chart-generator)
- [Chart Generator schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, API calls, files]

**Output Format:** [Markdown instructions with JSON call examples; remote action responses return JSON with signed URLs or base64 chart image data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports PNG, SVG, PDF, and WebP chart outputs; stored files expire after 1-7 days.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
