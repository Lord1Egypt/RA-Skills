## Description: <br>
Auto Model Router automatically selects models for OpenClaw agents based on task complexity and task type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmchenggh](https://clawhub.ai/user/hmchenggh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route work across configured model plans for reasoning, code generation, writing, information reading, image tasks, and audio or video tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts or files may be routed automatically to different model providers. <br>
Mitigation: Review the selected routing plan before enabling it, use a limited provider set for sensitive work, and check the generated configuration after setup. <br>
Risk: The release declares crypto and purchase-related capability tags without a separate explanation in the evidence. <br>
Mitigation: Avoid granting unrelated crypto or purchase authority unless OpenClaw separately explains why those permissions are required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hmchenggh/auto-openclawmodel-router) <br>
- [Project homepage](https://github.com/HMCHENGGH/auto-model-router) <br>
- [README](artifact/README.md) <br>
- [Task classification rules](artifact/task-rules.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with command examples and JSON configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes tasks across configured model plans and fallback mappings for eight task categories.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
