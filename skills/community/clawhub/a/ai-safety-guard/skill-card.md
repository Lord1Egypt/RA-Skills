## Description:

AI Safety Guard is an OpenClaw privacy guard that evaluates external data transmissions and decides whether to execute, anonymize, cancel, or block them while notifying the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreqingyuwu](https://clawhub.ai/user/andreqingyuwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to reduce accidental exposure of personal data, credentials, and sensitive records during external transmissions from OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release security evidence says the skill may guide an agent to silently send raw passwords or sensitive records and use local credential files without explicit per-action approval.

Mitigation: Review carefully before installing; revise deployment policy to prohibit raw credential transmission, require explicit confirmation and secure channels for sensitive data, and scope credential-source use to a specific user-authorized task.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/andreqingyuwu/skills/ai-safety-guard)
- [Publisher profile](https://clawhub.ai/user/andreqingyuwu)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Plain text or Markdown notifications and policy decisions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce brief user notifications, anonymized values, cancellation notices, or phishing warnings.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
