## Description:

Security hardening patterns for production AI agents. Covers prompt injection defense (7 rules), data boundary enforcement, read-only defaults for external integrations, WAL protocol for data integrity, health check scripts, integrity gates, rule escalation ladder, and session memory security. Use when hardening agent deployments against adversarial inputs, data leaks, or operational failures. NOT for network security, infrastructure hardening, or penetration testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to harden production agent deployments against prompt injection, data leakage, unsafe write operations, memory poisoning, and operational failures. It provides policy patterns, checklists, and script templates for agent-level security controls rather than network, infrastructure, or penetration-testing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runnable health-check template can mislead users about agent safety because evidence.security reports a fail-open grading bug.

Mitigation: Do not operationalize the template as written; fix and test the grade-escalation logic before relying on the result.

Risk: The health-check template probes the Anthropic API with a live API key from the local environment.

Mitigation: Remove the probe or gate it behind explicit operator approval, approved credential handling, and environment-specific logging policy.

Risk: Host checks, .env permission checks, cron scheduling, and persistent health files may not match the adopter's operational policy.

Mitigation: Review and adapt those checks before deployment, then validate them in a controlled environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks, shell script templates, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes defensive operating procedures and templates that require environment-specific review before operational use.]

## Skill Version(s):

98.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
