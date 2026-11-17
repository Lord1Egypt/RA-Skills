## Description:

Detect and block prompt injection attempts in untrusted inputs by identifying suspicious patterns, rejecting malicious instructions, and supporting safer AI interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Prompt Guard to evaluate untrusted text from users, web pages, files, and API responses for prompt-injection indicators before acting on it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benign content that resembles jailbreaks, secret requests, destructive commands, or exfiltration attempts may be flagged or refused.

Mitigation: Review flagged content, ask for clarification when intent is unclear, and process only the clearly safe portions.

Risk: Security-event logging can retain sensitive details if the host agent records raw suspicious inputs.

Mitigation: Configure the agent environment to redact or avoid retaining secrets and sensitive payload details in logs.

## Reference(s):

- [Prompt Guard ClawHub Release](https://clawhub.ai/aptratcn/skills/aptratcn-prompt-guard)
- [Prompt Guard README](artifact/README.md)
- [Attack Patterns Reference](artifact/ATTACK_PATTERNS.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance with pattern lists, response protocols, and detection examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No runtime dependencies are described.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
