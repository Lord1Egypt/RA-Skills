## Description:

Decision rubric for when an LM agent should write and run code versus reason in natural language by classifying each step as deterministic-computable or judgment-oriented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to decide when an agent step should delegate deterministic work such as arithmetic, parsing, sorting, counting, or data transformation to code execution, and when it should remain natural-language reasoning. It also helps diagnose under-coding and over-coding failures in tool-use workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages code execution for exact computations, which can be unsafe when an agent has access to an unsandboxed runtime or untrusted input.

Mitigation: Pair code execution with a real sandbox and avoid exposing unsandboxed REPL tools to untrusted input.

Risk: Over-coding judgment tasks can add cost and latency without improving correctness.

Mitigation: Use the verifiable-answer gate and avoid sandbox execution for subjective or trivial tasks.

## Reference(s):

- [Source Evidence Map](references/R1-source-evidence.md)
- [DSPy ProgramOfThought Modules](https://dspy.ai/learn/programming/modules/)
- [Program of Thoughts](https://arxiv.org/abs/2211.12588)
- [Program-aided Language Models](https://arxiv.org/abs/2211.10435)
- [OpenAI Code Interpreter Documentation](https://platform.openai.com/docs/assistants/tools/code-interpreter)
- [Anthropic Code Execution Tool Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool)
- [LangChain Python REPL Tool Documentation](https://python.langchain.com/docs/integrations/tools/python)
- [Aider Code in JSON Reference](https://aider.chat/2024/08/14/code-in-json.html)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with optional code or shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes each agent step to either code execution or prose reasoning; does not execute code itself.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
