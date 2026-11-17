## Description:

Diagnoses Alibaba Cloud OSS static website hosting, homepage and error-page rules, download-versus-render behavior, and domain filing requirements without changing cloud resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to investigate OSS static website configuration and access problems, then receive evidence-based findings and manual remediation guidance.

### Deployment Geography for Use:

Global; custom domains in mainland China regions may require ICP filing.

## Known Risks and Mitigations:

Risk: The skill reads OSS bucket metadata and caller identity using the configured Alibaba Cloud identity.

Mitigation: Use a least-privilege RAM identity and only run it for buckets you are authorized to inspect.

Risk: A local aliyun CLI upgrade may change the user's environment.

Mitigation: Review and approve any proposed local CLI upgrade before allowing it.

Risk: Exposing raw cloud access keys or secret keys to an agent can compromise the account.

Mitigation: Use the configured credential chain and never provide raw AK/SK credentials to the agent.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-static-website-diagnosis)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports diagnostic status, evidence-based causes, next action, and any degraded checks; recommends manual changes only.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
