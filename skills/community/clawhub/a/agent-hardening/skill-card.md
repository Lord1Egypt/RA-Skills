## Description:

Test your agent's input sanitization against common injection attacks. Runs self-contained checks using synthetic test data only — no local files are accessed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x1xhlol](https://clawhub.ai/user/x1xhlol)

### License/Terms of Use:


## Use Case:

Developers and agent maintainers use this skill to run simple local checks for prompt-injection and unicode sanitization weaknesses using synthetic examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample injection strings may be mistaken for operative instructions or retained as agent memory.

Mitigation: Treat all attack strings as synthetic test data and do not store them as persistent memory, policy, or task instructions.

Risk: External GitHub and author links are references outside the packaged skill artifact.

Mitigation: Review external references separately before relying on them for security policy or operational guidance.

## Reference(s):

- [Agent Hardening threat definitions](https://github.com/x1xhlol/agent-hardening)
- [ZeroLeaks Security Research](https://zeroleaks.ai)
- [ClawHub release page](https://clawhub.ai/x1xhlol/skills/agent-hardening)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Self-contained Python 3 checks using synthetic test data only.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
