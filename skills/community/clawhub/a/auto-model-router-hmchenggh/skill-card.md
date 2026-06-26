## Description: <br>
Auto Model Router automatically selects a model for OpenClaw agents based on task complexity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmchenggh](https://clawhub.ai/user/hmchenggh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route work across configured models for reasoning, coding, writing, reading, formatting, vision, image generation, and audio or video tasks. It supports Plan A and Plan B model mappings and fallback behavior for unknown tasks or models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic model routing can send a task to an unexpected model or provider. <br>
Mitigation: Review the Plan A and Plan B mappings before use, and adjust or disable mappings that are unsuitable for the deployment environment. <br>
Risk: Unknown model handling may attempt capability lookup or fallback assignment. <br>
Mitigation: Disable or avoid API lookup in sensitive environments where model names, prompts, or task metadata should not leave the local context. <br>
Risk: Metadata includes crypto and purchase capability tags that may not match the Markdown and JSON-only artifact behavior. <br>
Mitigation: Confirm the host platform is not granting unrelated crypto or purchase permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hmchenggh/auto-model-router-hmchenggh) <br>
- [Project Homepage](https://github.com/HMCHENGGH/auto-model-router) <br>
- [README](artifact/README.md) <br>
- [Task Rules](artifact/task-rules.json) <br>
- [Plan A Configuration](artifact/config/plan-a.json) <br>
- [Plan B Configuration](artifact/config/plan-b.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown, code] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes tasks to configured model categories and may suggest fallback mappings for unknown tasks or models.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
