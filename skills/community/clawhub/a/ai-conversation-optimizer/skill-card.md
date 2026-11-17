## Description:

AI conversation optimization assistant that diagnoses issues in user prompts and provides actionable improvements, optimized prompt examples, and related prompt engineering tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laninga](https://clawhub.ai/user/laninga)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to improve prompts when an AI answer is unsatisfactory or when they want a clearer, more constrained question. It guides the agent to diagnose prompt weaknesses, select optimization strategies, and return improved prompt examples in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad requests about improving AI questions.

Mitigation: Use it when prompt optimization is intended, and review whether the user's request actually asks for prompt diagnosis or rewriting before applying the workflow.

Risk: The skill is written for Chinese-language prompt-improvement workflows and may not provide multilingual guidance on its own.

Mitigation: Adapt the generated guidance to the user's requested language and locale when the conversation is not in Chinese.

## Reference(s):

- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Prompt Engineering Guide (DAIR.AI)](https://www.promptingguide.ai/)
- [Chain-of-Thought Prompting](https://www.promptingguide.ai/techniques/cot)
- [Prompt Patterns](references/prompt-patterns.md)
- [Prompt Checklist](references/checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with diagnostic sections, recommendations, optimized prompt examples, and related tips]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance by default; no code execution, credential handling, persistence, or system access.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
