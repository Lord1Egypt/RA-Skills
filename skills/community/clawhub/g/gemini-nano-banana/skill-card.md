## Description: <br>
Auto-generated skill for gemini tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to invoke Gemini image-generation tools through OneKey Gateway, providing prompts and image settings to create image files and JSON status results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and image-generation requests through third-party API and gateway dependencies. <br>
Mitigation: Use a revocable API key and avoid sending private prompts, sensitive images, secrets, or regulated data unless external processing is acceptable. <br>
Risk: Generated files may be written to user-provided paths. <br>
Mitigation: Provide explicit safe output locations and review generated file paths before use. <br>
Risk: The skill depends on the OneKey Gateway npm package and the ai-agent-marketplace Python package. <br>
Mitigation: Install only if you trust OneKey Gateway and the listed npm and PyPI packages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AI-Hub-Admin/gemini-nano-banana) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [Skills Marketplace](https://www.deepnlp.org/store/skills) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON result objects with generated image file paths and optional CLI shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and an explicit safe output location for generated files.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
