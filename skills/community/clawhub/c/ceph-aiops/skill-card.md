## Description:

Operate and diagnose Ceph clusters through the ceph-mgr Dashboard API, with health analysis, resource inspection, and governed cluster changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT

## Use Case:

Developers and storage administrators use the skill to diagnose Ceph health and inspect cluster resources, or to request controlled operational changes through the Dashboard API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ceph write operations can permanently delete data, and claimed confirmation safeguards do not cover all agent tools.

Mitigation: Start with a dedicated read-only Dashboard account. Before any write, require approval outside the model for the exact cluster, resource, and change; use dry-run previews where available, and verify audit storage is available before relying on write operations.

Risk: The documentation says write operations have not been verified against a live cluster.

Mitigation: Verify endpoint permissions and operation behavior against a non-production cluster before relying on writes in production.

## Reference(s):

- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Capabilities](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup guide](artifact/references/setup-guide.md)
- [ClawHub release page](https://clawhub.ai/zw008/skills/ceph-aiops)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown text with cluster findings, explanations, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings and recommendations should reflect current tool results; proposed writes can affect live cluster data.]

## Skill Version(s):

0.14.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
