## Description:

Security engineering workflow for OpenClaw privilege governance and hardening. Use for least-privilege execution, approval-first privileged actions, idle timeout controls, port + egress monitoring, and ISO 27001/NIST-aligned compliance reporting with mitigations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fletcherfrimpong](https://clawhub.ai/user/fletcherfrimpong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to assess and harden OpenClaw privilege governance, approval-first elevated execution, port and egress controls, and ISO 27001/NIST-aligned compliance reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sudo runtime hook can create serious review concerns around persistent PATH changes, caller-controlled guard paths, and approval bypasses.

Mitigation: Install only after review; do not enable the sudo runtime hook until caller-controlled paths are removed, policy files fail closed, approval-state mutation is protected, and LaunchAgent PATH changes have explicit confirmation and rollback.

Risk: Privileged execution controls may be incomplete if policy files are absent or elevated paths bypass the guarded wrapper.

Mitigation: Make policy files mandatory for privileged actions and route every elevated operation through guarded_privileged_exec.py with explicit user approval.

Risk: Unapproved listening ports or outbound destinations can remain exposed when baselines are missing or incomplete.

Mitigation: Maintain reviewed approved_ports.json and egress_allowlist.json baselines, then review and remediate all unapproved port and egress findings.

## Reference(s):

- [Least-Privilege Policy For OpenClaw](references/least-privilege-policy.md)
- [Port Monitoring Policy For OpenClaw](references/port-monitoring-policy.md)
- [Compliance Controls Map](references/compliance-controls-map.json)
- [Approved Ports Template](references/approved_ports.template.json)
- [Command Policy Template](references/command-policy.template.json)
- [Egress Allowlist Template](references/egress-allowlist.template.json)
- [Prompt Policy Template](references/prompt-policy.template.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown status reports with inline shell commands and generated JSON or HTML assessment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include check IDs, status, risk, evidence, and concrete mitigations for security and compliance findings.]

## Skill Version(s):

0.1.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
