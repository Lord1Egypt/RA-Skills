## Description:

Deploy web apps with backend APIs, database, file storage, AI operations, authentication, realtime, and cron jobs. Use when the user asks to deploy or publish a website or web app and wants a public URL. Uses HTTP API via curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avimak](https://clawhub.ai/user/avimak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy, update, and manage web apps on AppDeploy through HTTP API calls. It supports apps that need public URLs, backend APIs, data storage, authentication, realtime behavior, AI operations, and scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and store an AppDeploy API key in a local .appdeploy file.

Mitigation: Create or review the API key deliberately, protect the .appdeploy file, and ensure it is excluded from source control.

Risk: The skill can upload project files to AppDeploy during deployment.

Mitigation: Inspect deployment files and upload manifests before use, and exclude secrets, credentials, and local-only files from uploads.

## Reference(s):

- [AppDeploy ClawHub Skill Page](https://clawhub.ai/avimak/skills/appdeploy)
- [AppDeploy MCP API Endpoint](https://api-v2.appdeploy.ai/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployment manifests, API request payloads, app files, status checks, and remediation guidance.]

## Skill Version(s):

1.0.8 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
