## Description: <br>
Auto Model Router automatically selects an OpenClaw model for a task category based on task complexity, available models, and configured routing plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmchenggh](https://clawhub.ai/user/hmchenggh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route prompts across reasoning, coding, writing, reading, simple transformation, image, and audio or video task categories. It helps users configure international, China-focused, or GLM-based model plans and choose fallback behavior when a task or model is unknown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic model and provider selection can send sensitive prompts to a provider the user did not intend to use. <br>
Mitigation: Configure an allowlist for approved models and providers before using the router with sensitive prompts. <br>
Risk: Fallback and sub-agent behavior can select paid or unexpected providers when a task or model is unknown. <br>
Mitigation: Disable or limit fallback and sub-agent routing where the host supports it, and review provider choices before allowing paid usage. <br>
Risk: Runtime behavior that performs API lookups, writes configuration, reloads OpenClaw, or changes routing can affect privacy and control. <br>
Mitigation: Review any runtime implementation before granting permissions for API lookups, configuration writes, reloads, or paid provider usage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hmchenggh/auto-model-router-glm) <br>
- [Project homepage](https://github.com/HMCHENGGH/auto-model-router) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown with JSON configuration examples and inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes tasks across eight categories and may propose fallback or sub-agent handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
