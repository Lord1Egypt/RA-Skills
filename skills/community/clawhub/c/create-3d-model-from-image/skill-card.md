## Description:

Creates and refines 3D models from images or text prompts through AgentPMT-hosted remote tool calls, then retrieves completed model assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to create 3D assets from source images or text prompts, refine text-generated drafts, poll task status, and retrieve downloadable model files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, and texture guidance are sent to a remote AgentPMT service.

Mitigation: Do not send secrets, private wallet material, confidential assets, or unnecessary personal data in prompts, URLs, logs, or request bodies.

Risk: Setup examples include unpinned install commands and the skill freshness note says to reinstall after seven days.

Mitigation: Install from ClawHub/OpenClaw or a pinned, reviewed source, and refresh the skill before production use when the local copy is stale.

Risk: Model creation and refinement actions consume AgentPMT credits.

Mitigation: Confirm current credit costs and account budget before submitting generation or refinement requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/create-3d-model-from-image)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/create-3d-model-from-image)
- [3D Modeling Agent Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide asynchronous AgentPMT calls that can return task IDs, status, progress, settings, and model download URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
