## Description:

Provides OneKey Gateway tools for generating images with Gemini/Nano Banana image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke Gemini image generation through OneKey Gateway and save generated images from prompt, model, aspect ratio, and image size inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a OneKey Gateway API key and routes prompts or image inputs through the OneKey/Gemini provider path.

Mitigation: Use a dedicated, revocable API key and only submit prompts or images appropriate for that provider path.

Risk: Gateway dependencies are documented without pinned versions.

Mitigation: Pin and review npm and Python dependency versions before installing or deploying the skill.

Risk: The documentation includes image-analysis examples that are outside the two artifact scripts.

Mitigation: Review available tools and intended permissions before enabling the skill in an agent environment.

## Reference(s):

- [Gemini Nano Banana ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/gemini-nano-banana)
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router)
- [AI Agent Marketplace GitHub Repository](https://github.com/aiagenta2z/ai-agent-marketplace)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [JSON responses and generated image files, with Markdown and shell command guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image results may include image_path, image_url, message, and success fields.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
