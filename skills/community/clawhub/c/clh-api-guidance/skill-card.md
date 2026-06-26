## Description: <br>
ClawHub API Guidance helps developers understand ClawHub API authentication, endpoints, request examples, rate limits, error handling, and security practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason7602](https://clawhub.ai/user/jason7602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate with ClawHub APIs, build catalog or package tooling, inspect security metadata, and handle authenticated API workflows safely. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated examples may expose or misuse ClawHub API tokens. <br>
Mitigation: Use least-privilege tokens, store credentials in environment variables, rotate tokens regularly, and avoid hardcoding secrets. <br>
Risk: Write, delete, transfer, or admin API examples can change account, skill, package, or ownership state. <br>
Mitigation: Review every state-changing request before execution and require explicit approval for destructive or administrative operations. <br>
Risk: API guidance can become stale as endpoints, limits, or response shapes change. <br>
Mitigation: Check current ClawHub API behavior before production use and test integrations against non-destructive endpoints first. <br>


## Reference(s): <br>
- [ClawHub API Guidance skill page](https://clawhub.ai/jason7602/clh-api-guidance) <br>
- [ClawHub](https://clawhub.ai) <br>
- [API reference](artifact/reference/api-reference.md) <br>
- [Data models](artifact/reference/data-models.md) <br>
- [Enums](artifact/reference/enums.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP, curl, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may include authenticated ClawHub API calls that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
