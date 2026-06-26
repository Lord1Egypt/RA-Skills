## Description: <br>
Generate and iteratively edit images. Supports storage, UI for manual editing, history, version branching, time travel, reference images, and multiple AI models and providers with your own API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kivS](https://clawhub.ai/user/kivS) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use babbleBrush to create, edit, branch, inspect, and manage image canvases through the babbleBrush API. It is suited for workflows that need iterative image generation or editing with reference images, version history, and user-provided provider keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a BABBLEBRUSH_API_KEY and can guide authenticated requests involving user images, prompts, edit history, and configured provider credentials. <br>
Mitigation: Keep BABBLEBRUSH_API_KEY secure, install only if BabbleBrush is trusted with that data, and use scoped provider keys where possible. <br>
Risk: The documented API includes credential-management and canvas deletion actions. <br>
Mitigation: Require explicit user confirmation before adding provider credentials, removing provider credentials, or deleting canvases. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kivS/babblebrush) <br>
- [babbleBrush Website](https://babblebrush.com) <br>
- [babbleBrush API Reference](https://babblebrush.com/api) <br>
- [babbleBrush Claude Skill](https://babblebrush.com/babblebrush/claude/SKILL.md) <br>
- [babbleBrush OpenClaw Skill](https://babblebrush.com/babblebrush/openclaw/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BABBLEBRUSH_API_KEY for authenticated API requests.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
