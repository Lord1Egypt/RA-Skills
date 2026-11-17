## Description:

Get Firecrawl credentials and SDK setup into a project. Use when an application needs `FIRECRAWL_API_KEY`, when an agent should add Firecrawl to `.env`, when the user wants to authenticate Firecrawl for app code, or when choosing the first SDK and docs for a new Firecrawl integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to add Firecrawl credentials, environment configuration, SDK installation, and first integration guidance to new or existing application projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step runs a mutable third-party package with `@latest` and can bulk-install CLI tools and skills.

Mitigation: Verify the Firecrawl CLI package, consider pinning a known version, and review what `npx -y firecrawl-cli@latest init --all --browser` changes before relying on it.

Risk: The skill handles Firecrawl API credentials and may write them to `.env`.

Mitigation: Keep `.env` out of version control and logs, and prefer a project or platform secret manager when available.

Risk: Running setup in an arbitrary project can modify local configuration and dependency state.

Mitigation: Run setup only in a project context the user is comfortable modifying and review proposed file or dependency changes before committing them.

## Reference(s):

- [Firecrawl Homepage](https://www.firecrawl.dev)
- [Auth Flow](references/auth-flow.md)
- [SDK Installation](references/sdk-installation.md)
- [Project Setup](references/project-setup.md)
- [Firecrawl Node / TypeScript Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/node)
- [Firecrawl Python Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/python)
- [Firecrawl Rust Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/rust)
- [Firecrawl Java Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/java)
- [Firecrawl Elixir Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/elixir)
- [Firecrawl cURL / REST Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/curl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, dotenv, HTTP, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project file edits, SDK installation commands, environment variable configuration, and smoke-test steps.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact metadata says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
