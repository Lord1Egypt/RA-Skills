## Description:

Advanced prompt injection defense with multi-layer protection, memory integrity, and tool security wrapper. OWASP LLM Top 10 2026 compliant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add a high-priority security gate that screens agent inputs, memory/context loading, tool calls, and outputs for prompt-injection, memory-poisoning, credential-exfiltration, and leakage patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad control over agent flow and access to memory and identity files.

Mitigation: Install it only when a high-priority security gate is intended, and restrict file access to the minimum paths required by the deployment.

Risk: False positives, lockdown behavior, or context resets could interrupt legitimate work.

Mitigation: Test detection thresholds before production use and define an operator override and recovery process.

Risk: Optional webhook and agent-channel alerts could expose security-event metadata outside local storage.

Mitigation: Keep webhook delivery disabled unless needed, and review alert payloads and retention before enabling external monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/anti-injection-skill)
- [Skill homepage](https://github.com/georges91560/anti-injection-skill)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples, plus text security decisions, alerts, and local log entries during operation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can block or allow agent actions, adjust a security score, write local audit and incident files, and send optional alerts when configured.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
