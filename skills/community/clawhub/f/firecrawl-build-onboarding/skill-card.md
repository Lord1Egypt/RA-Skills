## Description: <br>
Get Firecrawl credentials and SDK setup into a project for applications that need Firecrawl API access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to authenticate Firecrawl, add required environment configuration, choose an SDK or REST path, and complete an initial project integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Firecrawl API key can be exposed if it is committed, logged, or pasted into shared contexts. <br>
Mitigation: Store FIRECRAWL_API_KEY only in ignored environment files or a deployment secret manager, avoid sharing it in logs or chats, and rotate it if exposure occurs. <br>


## Reference(s): <br>
- [Auth Flow](references/auth-flow.md) <br>
- [SDK Installation](references/sdk-installation.md) <br>
- [Project Setup](references/project-setup.md) <br>
- [Firecrawl](https://www.firecrawl.dev) <br>
- [Firecrawl Node / TypeScript Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/node) <br>
- [Firecrawl Python Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/python) <br>
- [Firecrawl Rust Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/rust) <br>
- [Firecrawl Java Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/java) <br>
- [Firecrawl Elixir Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/elixir) <br>
- [Firecrawl REST Agent Source of Truth](https://docs.firecrawl.dev/agent-source-of-truth/curl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, dotenv, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of FIRECRAWL_API_KEY and optional FIRECRAWL_API_URL before SDK or REST integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
