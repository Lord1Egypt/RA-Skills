## Description:

Helps deploy static sites to Aliyun OSS with custom-domain HTTPS, GitHub Actions deployment, and certificate renewal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to publish static sites to Aliyun OSS, configure a custom domain and HTTPS certificate, and automate deployment and renewal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing the wrong build or changing OSS public access can expose private or unreviewed content.

Mitigation: Confirm the exact output directory, bucket, and domain; review the public build and access settings before deploying.

Risk: Stored GitHub credentials or broad Aliyun permissions can grant excessive access when configuring automation.

Mitigation: Supply a narrowly scoped token through GITHUB_TOKEN, avoid the stored-credential fallback, and use a least-privilege Aliyun RAM account.

Risk: Certificate, DNS, and GitHub Actions operations can change live services or repository settings.

Mitigation: Confirm the target domain, repository, secret and variable names before write or delete operations; test on a nonproduction bucket and subdomain first.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oracis/skills/aliyun-oss-static-deploy-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide changes to live OSS, DNS, certificate, and GitHub Actions settings.]

## Skill Version(s):

1.1.4 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
