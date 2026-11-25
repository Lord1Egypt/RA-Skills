## Description:

Deploys a local web project to the WEB DEPLOY platform with appcli and returns the address it opens at. Makes the project ready (Dockerfile, deploy.manifest.json, health check), has the platform build and run it (no Docker and no server access on this computer), and repairs and retries from what the server reports. Use when the user asks to deploy, publish, launch or put online a website, web application or backend API (部署、上线、发布、发到服务器), and for anything about a project deployed this way - its status or logs, a site that does not open or is asleep, runtime parameters, rolling back, restoring a backup, public access or the domain prefix, deleting it, plan limits, an appcli command or error code, or deploy.manifest.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lageai](https://clawhub.ai/user/lageai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare and deploy a local web application or API through the WEB DEPLOY platform, then manage its status, logs, settings, backups, and related deployment issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it flags advice about Secure cookies.

Mitigation: Review the cookie guidance before applying it and check the resulting cookie behavior for the deployed application.

Risk: ClawScan reports possible vulnerabilities in the example dependency; its scan was partial and does not establish that all related material was assessed.

Mitigation: Verify the dependency report and review the example material before relying on it; treat unresolved paths as unassessed.

## Reference(s):

- [appcli reference](references/appcli-reference.md)
- [Operations guide](references/operations.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Runtime parameter guide](references/personal-configuration.md)
- [Build base images](references/base-images.md)
- [Stack conventions](references/stacks.md)
- [Next.js and SQLite example](references/example-nextjs-sqlite/README.md)
- [ClawHub skill page](https://clawhub.ai/lageai/skills/code-agent-deploy)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands, Deployment status and access URL]

**Output Format:** [Markdown guidance with shell commands, code and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific deployment steps and status; a deployment URL is returned when deployment succeeds.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
