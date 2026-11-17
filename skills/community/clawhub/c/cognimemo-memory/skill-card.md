## Description:

CogniMemo Memory helps agents store, retrieve, update, and delete persistent memory such as preferences, decisions, tasks, facts, and context across AI applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to persistent memory workflows, including storing user preferences, decisions, tasks, and facts, then retrieving relevant context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can store broad user and conversation context outside the current session without strong opt-in or scoping.

Mitigation: Require explicit user opt-in before capture, scope access by memory type and user, and provide revocation and deletion controls.

Risk: Secrets or highly sensitive personal data could be stored in reusable memory.

Mitigation: Filter or redact secrets and sensitive data before storage, and document categories that must not be saved.

Risk: Example integrations rely on caller-side permission checks and external API keys.

Mitigation: Enforce permission checks in integration code, use least-privileged environments, pin SDK versions, and keep API keys in environment variables.

## Reference(s):

- [CogniMemo Memory ClawHub Skill](https://clawhub.ai/engsathiago/skills/cognimemo-memory)
- [CogniMemo Website](https://cognimemo.com)
- [CogniMemo Documentation](https://docs.cognimemo.com)
- [CogniMemo API Reference](https://api.cognimemo.com/docs)
- [CogniMemo SDK GitHub Repository](https://github.com/cognimemo/sdk)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CogniMemo API key for real external integration; the included memory_manager.py script uses mock storage for demonstration.]

## Skill Version(s):

1.0.0 (source: evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
