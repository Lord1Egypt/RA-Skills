## Description:

AI-powered memory system that compresses, reflects on, and retrieves past agent actions to improve long-term autonomous decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building persistent autonomous agents use this skill to store experiences, generate delayed reflections, query prior outcomes, and inspect memory statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent experiences are saved in plaintext local storage and may contain sensitive context, results, or user details.

Mitigation: Run the skill in a private project directory, avoid storing secrets or regulated data, and delete memory_store.json when retained history is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/agent-reflective-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included CLI stores and retrieves local memory entries in a plaintext JSON file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
