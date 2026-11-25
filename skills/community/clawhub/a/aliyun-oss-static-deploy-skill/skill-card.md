## Description:

Deploys static sites to Alibaba Cloud OSS with custom domains, HTTPS certificates, GitHub Actions automation, and certificate renewal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oracis](https://clawhub.ai/user/oracis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to publish static site builds to Alibaba Cloud OSS, configure custom domains and HTTPS, and automate deployments and certificate renewal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags potentially destructive behavior in dry-run handling.

Mitigation: Review proposed file and cloud changes before execution, and start with a test bucket or subdomain.

Risk: Files reached through symlinks may be included in publication.

Mitigation: Inspect resolved upload paths and exclude symlinked files unless their publication is explicitly intended.

Risk: The skill includes plaintext credential storage guidance.

Mitigation: Keep credentials in environment variables or a secrets manager, use least-privilege keys, and avoid writing secrets to files.

Risk: Certificate automation may change Function Compute custom domains beyond the stated deployment target.

Mitigation: Specify target domains explicitly and review the existing domain configuration before applying certificate updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oracis/skills/aliyun-oss-static-deploy-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown instructions with shell commands, Python scripts, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deployment and verification steps; actions require cloud credentials and may change DNS, OSS, certificate, or Function Compute settings.]

## Skill Version(s):

1.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
