## Description: <br>
Azure Identity SDK for Python authentication guidance for DefaultAzureCredential, managed identity, service principals, and token caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thegovind](https://clawhub.ai/user/thegovind) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when implementing Azure SDK authentication in Python, choosing credentials for local development, CI/CD, and Azure-hosted workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Azure credential material could be exposed if users paste secrets into prompts or logs. <br>
Mitigation: Avoid sharing secrets with the agent; use managed identities or environment variables and redact sensitive values. <br>
Risk: Over-privileged identities or unpinned dependencies can increase production exposure. <br>
Mitigation: Use least-privilege Azure identities and pin the azure-identity dependency in production projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thegovind/azure-identity-py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Azure credential examples and environment-variable guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
