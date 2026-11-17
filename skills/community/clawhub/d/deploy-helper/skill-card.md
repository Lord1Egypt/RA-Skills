## Description:

One-command deployment assistant. Generate Dockerfiles, docker-compose configs, Nginx configs, CI/CD pipelines, Vercel/Netlify configs, Kubernetes manifests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and engineers use Deploy Helper to generate copy-and-review deployment configuration and command guidance for containers, web servers, CI/CD, serverless hosting, Kubernetes, and SSL setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker Compose examples include insecure default database credentials.

Mitigation: Replace all database credentials with real secrets or environment-based secret management before use.

Risk: The unrelated script.sh records local command history under the user's deploy-helper data directory.

Mitigation: Do not run script.sh unless local command-history logging is acceptable, or remove the logging behavior before installation.

Risk: The SSL guidance includes privileged certbot and package-manager commands.

Mitigation: Treat SSL output as copy-and-review guidance and run adapted commands manually only after confirming the target host and domain.

Risk: Generated deployment templates may not match the target application's runtime, secret, networking, or production requirements.

Mitigation: Review, test, and scan generated configuration before applying it to any deployed environment.

## Reference(s):

- [Deploy Helper on ClawHub](https://clawhub.ai/xueyetianya/skills/deploy-helper)
- [xueyetianya publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text containing deployment templates, code blocks, YAML/TOML/JSON snippets, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated as copy-and-review templates; the skill does not deploy infrastructure by itself.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
