## Description:

Cross-cloud security posture assessment covering IAM analysis, encryption audit, and public exposure detection across AWS, Azure, and GCP using [AWS]/[Azure]/[GCP] inline labels for provider-specific commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud security engineers, and auditors use this skill to assess IAM, encryption, and public exposure posture across AWS, Azure, and GCP environments. It supports multi-cloud reviews, pre-compliance audits, migration gates, incident-response scoping, periodic checks, and due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags an overbroad GCP storage admin prerequisite despite the skill's read-only posture.

Mitigation: Use the narrowest read-only or custom GCP permissions that can list buckets and read IAM policies instead of granting storage admin.

Risk: Production cloud assessment can expose sensitive posture details or run low-impact initiation commands.

Mitigation: Review commands before use, run them with a dedicated short-lived audit identity, and treat aws iam generate-credential-report as an explicit initiation step.

## Reference(s):

- [Cloud Security Posture skill page](https://clawhub.ai/vahagn-madatyan/skills/cloud-security-posture)
- [CLI Reference](references/cli-reference.md)
- [Security Controls Reference](references/security-controls.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and assessment tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only assessment guidance and report content for agent-mediated cloud security reviews.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
