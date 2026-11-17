## Description:

Security engineering workflow for OpenClaw privilege governance and hardening. Use for least-privilege execution, approval-first privileged actions, idle timeout controls, port and egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fletcherfrimpong](https://clawhub.ai/user/fletcherfrimpong)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to review OpenClaw privilege controls, enforce approval-first elevation, monitor listening ports and outbound connections, and produce ISO 27001/NIST-aligned findings with mitigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a persistent sudo wrapper that changes how OpenClaw privileged commands are routed.

Mitigation: Install only when that routing is intentional, require reviewed command policy files first, and remove or replace the sudo PATH shim if it is not acceptable for the deployment.

Risk: Approval, session state, and environment handling may be weak if local files are writable, overly broad, or not scoped to the active task.

Mitigation: Make approval state unforgeable, restrict env-file parsing to required flags, enforce task session IDs and approval tokens where appropriate, and harden file permissions.

Risk: Notification execution and audit logging can expose operational risk if commands or logs are not controlled.

Mitigation: Eliminate shell-based notifier execution, protect and redact audit logs, and keep privileged audit records append-only where possible.

Risk: Network and command baselines may be missing or incomplete, causing privileged actions, listening ports, or outbound connections to bypass intended review.

Mitigation: Populate and review command policy, approved ports, prompt policy, and egress allowlist files before relying on enforcement.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fletcherfrimpong/skills/fletcher-cyber-security-engineer)
- [Least-Privilege Policy For OpenClaw](references/least-privilege-policy.md)
- [Port Monitoring Policy For OpenClaw](references/port-monitoring-policy.md)
- [Compliance Controls Map](references/compliance-controls-map.json)
- [Command Policy Template](references/command-policy.template.json)
- [Egress Allowlist Template](references/egress-allowlist.template.json)
- [Prompt Policy Template](references/prompt-policy.template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown status reports, JSON and HTML assessments, shell commands, configuration templates, and Python/Bash code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should include affected check_id values, status, risk, concise evidence, and concrete mitigations.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
