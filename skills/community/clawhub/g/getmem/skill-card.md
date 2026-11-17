## Description:

getmem.ai Memory provides persistent memory for AI agents through getmem.ai by retrieving relevant context before model calls and ingesting conversation turns afterward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimblev2023](https://clawhub.ai/user/nimblev2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent, semantically retrieved memory to AI agents while reducing the need to send full conversation history on every turn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends conversation content to getmem.ai for indefinite third-party storage.

Mitigation: Use only with appropriate consent, redaction, retention controls, and a way to inspect and delete stored memories.

Risk: Retrieved memories are injected into a privileged prompt context and may influence future agent behavior.

Mitigation: Review retrieved memory before privileged use and avoid storing credentials, regulated data, private customer data, or proprietary code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nimblev2023/skills/getmem)
- [getmem.ai website](https://getmem.ai)
- [getmem.ai platform](https://platform.getmem.ai)
- [getmem-ai on PyPI](https://pypi.org/project/getmem-ai/)
- [getmem on npm](https://npmjs.com/package/getmem)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes API key setup and examples for retrieving and ingesting memory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
