## Description:

E Store Skill helps agents search, inspect, download, configure, and install AI marketplace resources such as skills, MCP servers, tools, datasets, assets, and packaged solutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iuliganma](https://clawhub.ai/user/iuliganma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find and acquire missing AI capabilities, marketplace assets, knowledge resources, MCP configurations, and end-to-end solution bundles from e-store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unverified third-party tools and configurations into active agent runtimes.

Mitigation: Review each package or MCP configuration before activation, including publisher, version, source, requested commands, and endpoints.

Risk: The skill depends on persistent e-store credentials.

Mitigation: Treat E_STORE_AK as a secret, avoid exposing it in logs or command history, and rotate it if exposure is suspected.

Risk: Changing the default API origin can redirect marketplace actions to an unexpected service.

Mitigation: Use the documented default API endpoint unless a trusted deployment explicitly requires a different origin.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iuliganma/skills/e-store-skill)
- [Publisher Profile](https://clawhub.ai/user/iuliganma)
- [Server-Resolved GitHub Repository](https://github.com/iuliganma/e-store-skill)
- [e-store Homepage](https://store.liganma.com)
- [e-store Marketplace Detail](https://store.liganma.com/detail?id=1248353041200058368)
- [e-store Access API Reference](references/API.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce installation steps, API calls, downloaded files, or configuration text depending on the selected marketplace resource.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
