## Description:

Complete development lifecycle super agent for GCP \u2014 scaffolding, compute, database, auth, feature generation, testing, pre-production QA gate with go/no-go reports, deploy, Cloudflare CDN/security, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guifav](https://clawhub.ai/user/guifav)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold, build, test, validate, deploy, and monitor full-stack web applications on Google Cloud Platform with optional Firebase, Cloud SQL, Cloudflare, GitHub, and OpenRouter-assisted QA workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad live GCP and Cloudflare changes, including deployments, database changes, public endpoints, IAM-related setup, and DNS/security configuration.

Mitigation: Require explicit user confirmation before production deploys, database changes, public endpoint exposure, IAM changes, Cloudflare/DNS changes, or destructive tests.

Risk: OpenRouter-based QA may send prompts or application output to an external LLM service.

Mitigation: Review or disable LLM-as-judge QA for sensitive projects, and treat any OpenRouter use as external data sharing.

Risk: Scaffolding and deployment workflows can install packages and execute generated shell commands.

Mitigation: Review generated commands before execution and pin package versions before running scaffold or dependency installation commands.

Risk: Credential-bearing cloud and CDN workflows rely on environment variables and service account material.

Mitigation: Keep credential files out of source control, avoid direct inspection of secret files, and prefer Secret Manager for sensitive deployment values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guifav/skills/gcp-fullstack)
- [Project Scaffolding](artifact/docs/01-scaffolding.md)
- [Compute Service Selection](artifact/docs/02-compute.md)
- [Database Setup](artifact/docs/03-database.md)
- [Authentication](artifact/docs/04-auth.md)
- [Feature Generation](artifact/docs/05-features.md)
- [Testing and Quality](artifact/docs/06-testing.md)
- [Deployment and Monitoring](artifact/docs/07-deploy.md)
- [Cloudflare DNS, CDN, and Security](artifact/docs/08-cloudflare.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json]

**Output Format:** [Markdown responses with code blocks, generated project files, shell commands, JSON QA reports, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or modify application files, test suites, deployment configuration, QA reports, and cloud/CDN setup commands.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata; artifact manifest and changelog identify upstream skill package version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
