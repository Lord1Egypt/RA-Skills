## Description:

AI cognitive flexibility with four cognitive modes, automatic mode switching, and metacognitive monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alpha963852](https://clawhub.ai/user/alpha963852)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add mode selection, chain reasoning, pattern matching, creative exploration, hypothesis generation, and self-assessment to complex agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store raw task and context data in plaintext local logs when monitoring is enabled.

Mitigation: Disable monitoring for sensitive work, avoid passing private prompts or customer data, and delete or restrict access to the logs directory.

Risk: The requested tool permissions are broader than the core reasoning purpose requires.

Mitigation: Grant only the tools needed for a deployment and remove unused permissions such as Write, Edit, sessions_send, and web_search unless a reviewed workflow requires them.

Risk: Retrieved memories or task context may influence reasoning results and expose sensitive context in outputs or logs.

Mitigation: Review memory sources before use and keep private data out of task descriptions and context objects.

## Reference(s):

- [OODA Mode Guide](references/ooda-guide.md)
- [Cognitive Flexibility Repository](https://github.com/openclaw/skills/cognitive-flexibility)
- [README Documentation](https://github.com/openclaw/skills/cognitive-flexibility/blob/main/README.md)
- [ClawHub Skill Page](https://clawhub.ai/alpha963852/skills/cognitive-flexibility)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, code examples, and structured runtime results with answers, reasoning chains, confidence scores, and monitoring reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local plaintext usage logs and aggregate statistics when monitoring is enabled.]

## Skill Version(s):

2.1.0 (source: target metadata, SKILL.md frontmatter, clawhub.yaml, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
