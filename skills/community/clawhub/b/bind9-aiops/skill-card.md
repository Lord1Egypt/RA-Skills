## Description:

Use this skill when a user needs to inspect a BIND 9 DNS server, validate zones, diagnose SERVFAIL, inspect DNSSEC and stale-answer status, compare SOA serials, or request a zone reload, refresh, secondary retransfer, NOTIFY resend or name-specific cache flush. It requires local rndc, named-checkconf and dig utilities and appropriate server-side permissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DNS engineers use the skill to inspect BIND 9 service, configuration, zones, DNSSEC, and primary/secondary SOA state. They can also request guarded zone reload, refresh, retransfer, NOTIFY, or name-specific cache flush operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reload, refresh, retransfer, NOTIFY, and cache-flush operations can affect live DNS service or cache state.

Mitigation: Use dry-run and grant the process only the RNDC permissions needed for intended operations; check BIND zone status and SOA after an unknown write outcome before retrying.

Risk: SOA comparisons can be misread when a response is not authoritative or a probe fails.

Mitigation: Confirm the query is authoritative for the intended zone, check diagnostic error and completion fields, and treat serial equality as equality only rather than serial ordering.

## Reference(s):

- [BIND 9 AIops repository](https://github.com/AIops-tools/BIND9-AIops)
- [ClawHub release page](https://clawhub.ai/zw008/skills/bind9-aiops)
- [Agent guardrails](references/agent-guardrails.md)
- [Capabilities](references/capabilities.md)
- [CLI reference](references/cli-reference.md)
- [Setup guide](references/setup-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Configuration instructions]

**Output Format:** [Structured DNS diagnostic results and operational guidance as JSON or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report incomplete or unknown results; write operations support dry-run and can have an unknown outcome.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
