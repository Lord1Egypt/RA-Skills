## Description:

Provides a curated Chinese-language learning guide and simple chatbot stub for AI agent development with large language models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to find Bilibili learning resources for building LLM-based AI agents, from introductory concepts through practical development. The included executable stub can also return simple text responses for greeting, goodbye, and fallback prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable Python file inserts a hard-coded local directory into the module search path, which could allow local import hijacking if that directory is writable by untrusted users.

Mitigation: Remove the hard-coded sys.path insertion before use, or run the skill only in an environment where the referenced local path cannot be modified by untrusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/auto-llm-4891)
- [Bilibili: OmniRoute LLM access video](https://www.bilibili.com/video/BV1W9DUBMEVs)
- [Bilibili: ComfyUI local LLM prompt-polishing video](https://www.bilibili.com/video/BV1e8TSzhEgT)
- [Bilibili: LLM MoE expert parallelism video](https://www.bilibili.com/video/BV1W314BfEHr)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance and plain text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No structured output contract; the Python stub returns a single text string.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
