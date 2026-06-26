## Description: <br>
AI对话优化助手。诊断用户提问中的问题，给出可执行的改进方案和优化后的prompt示例。覆盖角色设定、Few-shot、CoT、格式指定等核心技巧。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laninga](https://clawhub.ai/user/laninga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to diagnose unclear or underspecified prompts, then produce improved prompts with role, context, scope, format, Few-shot, and reasoning-pattern guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste secrets or private data while asking for prompt improvements. <br>
Mitigation: Review and redact sensitive prompt content before using the skill. <br>
Risk: The skill may activate on broad questions about AI answer quality. <br>
Mitigation: Confirm the user wants prompt coaching before applying the full optimization workflow. <br>


## Reference(s): <br>
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) <br>
- [Prompt Engineering Guide (DAIR.AI)](https://www.promptingguide.ai/) <br>
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot) <br>
- [Prompt 提问检查清单](references/checklist.md) <br>
- [常见 Prompt 模式](references/prompt-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured diagnostic sections and prompt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompt diagnoses, optimization suggestions, revised prompts, and brief related technique notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
