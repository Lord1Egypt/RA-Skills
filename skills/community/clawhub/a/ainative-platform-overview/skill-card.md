## Description:

Top-level discovery skill for the entire AINative platform, helping users understand platform capabilities, choose APIs or SDKs, get started, and route to specialized skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a top-level guide to the AINative platform when evaluating APIs, SDKs, MCP servers, authentication options, package choices, and related skills for deeper implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests unpinned package installation commands and global npm installs that can modify a user's development environment.

Mitigation: Verify publisher and package versions before installation, prefer pinned versions and project-local installs, and avoid running setup commands with administrator privileges.

Risk: The `zerodb init` setup command may change local project or IDE configuration.

Mitigation: Review what the command will modify before running it and execute it in a controlled project workspace.

## Reference(s):

- [AINative API Base URL](https://api.ainative.studio)
- [AINative Chat Completions Endpoint](https://api.ainative.studio/v1/public/chat/completions)
- [API Reference](docs/api/API_REFERENCE.md)
- [Quick Start](docs/guides/QUICK_START.md)
- [Authentication Guide](docs/guides/AUTHENTICATION.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with tables and inline bash, curl, and package-install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes users to related AINative skills and summarizes package, API, authentication, and setup options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
