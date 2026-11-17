## Description:

Looks up and summarizes legal and operational risk records for mainland China companies using a company name, unified social credit code, or companyId.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and compliance reviewers use this skill to query mainland China company risk records and receive a structured markdown risk overview plus a concise agent-written risk summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company identifiers and risk-query activity to an external 1688/OpenClaw service.

Mitigation: Install only if that integration is trusted and users are comfortable sharing the queried company identifiers with the service.

Risk: Access-key configuration and fallback storage can persist credentials under a shared cha88-base configuration namespace.

Mitigation: Protect the OpenClaw configuration file, review who can read it, and rotate or remove the key when it is no longer needed.

Risk: A misconfigured OpenClaw gateway URL could send configuration requests to an untrusted local endpoint.

Mitigation: Before configuring an access key, confirm OPENCLAW_GATEWAY_URL points only to a trusted local gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-common-cha88-company-risk)
- [Company risk capability guide](artifact/references/capabilities/companyRisk.md)
- [Company search capability guide](artifact/references/capabilities/cha88_search.md)
- [Access key configuration guide](artifact/references/capabilities/configure.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [JSON containing a markdown field, followed by agent-authored markdown risk analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and an ACCESS_KEY-compatible 1688/OpenClaw credential for live queries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
