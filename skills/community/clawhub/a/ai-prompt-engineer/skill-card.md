## Description:

A comprehensive prompt engineering skill for AI developers building LLM-powered applications. Covers system prompt design, few-shot prompting, chain-of-thought reasoning, tool-use patterns, structured output enforcement, context management, prompt templates, evaluation frameworks, multi-turn conversation handling, multimodal prompting, agent patterns such as ReAct and plan-and-execute, and safety guardrails including prompt injection defence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royhk920](https://clawhub.ai/user/royhk920)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to craft, debug, and evaluate prompts for LLM-powered applications, including system prompts, structured outputs, tool use, agent patterns, multimodal prompting, and safety guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example evaluators can send prompts, outputs, and test inputs to OpenAI.

Mitigation: Run evaluations only with non-sensitive test data and review prompts before using real user or business content.

Risk: The example evaluation setup installs and imports the openai package without a pinned version.

Mitigation: Use a virtual environment and pin the openai package version for reproducible evaluation behavior.

Risk: The scaffold script creates local project files and an environment template.

Mitigation: Review generated files before use and keep real .env secrets out of source control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/royhk920/skills/ai-prompt-engineer)
- [System prompt examples](artifact/examples/system-prompts.md)
- [Prompt evaluation framework example](artifact/examples/evaluation-framework.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt templates, code examples, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples include local scaffold generation and OpenAI-based evaluation scripts.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
