## Description:

Detect AI API/provider/model failures and route requests to healthy fallback providers or downgraded models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zqh2333](https://clawhub.ai/user/zqh2333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or maintain a local AI API failover layer with provider health checks, circuit breakers, guarded retries, profile-aware routing, and model downgrade paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local proxy can expose credential-backed model access through an unauthenticated HTTP service.

Mitigation: Keep the proxy bound to 127.0.0.1 unless real authentication, authorization, and network controls are added.

Risk: Prompts may be forwarded to each configured upstream provider in the routing chain.

Mitigation: Review provider configuration and fallback order before use, and route sensitive workloads only to approved providers.

Risk: Temporary file handling and health endpoint exposure were flagged as areas needing hardening before elevated or shared deployments.

Mitigation: Run without elevated privileges and harden temporary file paths and health endpoint exposure before broader deployment.

## Reference(s):

- [API Failover Skill Page](https://clawhub.ai/zqh2333/skills/api-failover)
- [Production Configuration Template](references/config-production.yaml)
- [Real-world Setup Notes](references/realworld-notes.md)
- [Activation Checklist](references/activation-checklist.md)
- [Test Scenarios](references/test-scenarios.md)
- [Delivery Summary](references/delivery-summary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration examples, Python scripts, shell commands, and JSON health or self-check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local proxy routing behavior and configuration guidance; runtime results depend on configured upstream providers and credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
