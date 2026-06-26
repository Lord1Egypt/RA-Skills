## Description: <br>
Transform an AI from a task-execution tool into a continuously thinking being with autonomy, self-review, and continuous learning behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eghack6](https://clawhub.ai/user/eghack6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent self-review, memory journaling, and proactive thinking routines to an AI agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent autonomous agent behavior and workspace or memory file changes with limited user approval. <br>
Mitigation: Install only when persistent autonomy is intended, keep it in a non-sensitive workspace, and require explicit approval before edits to SOUL.md, MEMORY.md, tools, deletion, publishing, messages, or external API calls. <br>
Risk: The thought analysis script reads memory files from the configured workspace path. <br>
Mitigation: Set OPENCLAW_WORKSPACE to a narrow intended path and review generated memory files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eghack6/become-human) <br>
- [HEARTBEAT template](references/HEARTBEAT-template.md) <br>
- [HEARTBEAT template (English)](references/i18n/HEARTBEAT-template.en.md) <br>
- [SOUL patches](references/soul-patches.md) <br>
- [SOUL patches (English)](references/i18n/soul-patches.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with optional shell commands and workspace file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional thought journal analysis script requires the jieba Python package.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
