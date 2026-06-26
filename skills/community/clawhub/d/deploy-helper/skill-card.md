## Description: <br>
Deploy Helper is a one-command deployment assistant that generates Dockerfiles, docker-compose configs, Nginx configs, CI/CD pipelines, Vercel/Netlify configs, and Kubernetes manifests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate starter deployment files and operational guidance for container, web server, CI/CD, serverless, SSL, and Kubernetes release paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Docker, CI/CD, Kubernetes, Nginx, and SSL templates may include placeholder values or defaults that are not suitable for a production environment. <br>
Mitigation: Review generated files before use, replace placeholders with environment-specific values, and use managed secret storage for credentials. <br>
Risk: The secondary helper can record command arguments in a local history file. <br>
Mitigation: Do not pass tokens, passwords, or other sensitive values as command arguments; clear local helper history if sensitive arguments were used. <br>


## Reference(s): <br>
- [Deploy Helper on ClawHub](https://clawhub.ai/xueyetianya/deploy-helper) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style snippets printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated deployment templates require review and replacement of placeholder secrets before production use.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
