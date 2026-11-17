## Description:

Guides the setup of GitHub Actions and Alibaba Cloud RAM OIDC to renew Let's Encrypt wildcard certificates and distribute them to CDN, OSS, or Function Compute without storing long-lived access keys in repository secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this guide and its scripts to configure GitHub Actions access to Alibaba Cloud, renew wildcard TLS certificates, and distribute them to cloud services without keeping long-lived access keys in repository secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cloud permissions could give the workflow more access than certificate renewal and distribution require.

Mitigation: Limit the RAM policy to required actions and resources, and review the permissions before deployment.

Risk: The OIDC trust rule may allow unrelated repositories to assume the cloud role.

Mitigation: Restrict the trust condition to the exact repository and protected branch, and verify its issuer, audience, and subject conditions.

Risk: The security review had partial scanner coverage, including partly inspected code and an image outside analyzer scope.

Mitigation: Review files and assets not fully covered by the scanners, then rerun the security review before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/oracis/skills/aliyun-oidc-cert-renew)
- [Project page listed in the skill documentation](https://github.com/oracis/aliyun-oidc-cert-renew)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python, YAML, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes certificate renewal and distribution workflows, troubleshooting guidance, and monthly verification steps.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
