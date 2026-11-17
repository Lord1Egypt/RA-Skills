## Description:

Diagnoses 1688 shop operating health by querying core peer-comparison metrics, traffic structure, industry transaction ranking, and customer profile data, then producing bottleneck analysis and improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect 1688 store performance, compare operational metrics against peers and industry benchmarks, and generate concise shop-health diagnostics with suggested improvement areas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles the user's 1688 AK credential and security evidence says command output can expose the AK.

Mitigation: Avoid running configure --status until AK masking is fixed; use the skill only on a trusted single-user machine and rotate the AK if it appears in chat, logs, screenshots, or command output.

Risk: Security evidence says the local authorization callback is network-reachable and can overwrite stored credentials.

Mitigation: Run authorization only on a trusted network, close the callback flow promptly after use, and verify or clear credentials after any unexpected authorization event.

Risk: The skill accesses 1688 shop and business metrics.

Mitigation: Review the skill before installation and limit use to accounts and environments where exposing shop operational data to the agent is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-shop-operate)
- [AK configuration guide](artifact/references/capabilities/configure.md)
- [Core metrics guide](artifact/references/capabilities/get_core_metrics.md)
- [Traffic structure guide](artifact/references/capabilities/get_traffic_structure.md)
- [Transaction ranking guide](artifact/references/capabilities/get_transaction_ranking.md)
- [Customer profile guide](artifact/references/capabilities/get_customer_profile.md)
- [Error handling guide](artifact/references/common/error-handling.md)
- [1688 AK portal](https://clawhub.1688.com/)
- [1688 skills gateway](https://skills-gateway.1688.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [JSON command results containing markdown and data fields, followed by Markdown diagnostic reporting and guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured AK credential and Python CLI execution; transaction ranking supports RECENT_7 and RECENT_30 only.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
