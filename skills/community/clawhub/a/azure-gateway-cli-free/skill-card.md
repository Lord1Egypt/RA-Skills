## Description: <br>
Azure Gateway Cli Free guides an agent through configuring a local proxy that adapts OpenAI-compatible requests to a user's Azure OpenAI deployment for local development and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use when a developer needs to connect OpenAI-compatible clients or agent tooling to a self-managed Azure OpenAI endpoint, configure local environment variables, run basic health checks, and troubleshoot common connection errors. <br>

### Deployment Geography for Use: <br>
Local developer environments; use is governed by the user's Azure OpenAI resource location and applicable organization policies. <br>

## Known Risks and Mitigations: <br>
Risk: Azure OpenAI API keys could be exposed through shared configs, repositories, or logs. <br>
Mitigation: Keep keys in environment variables or private local files, exclude those files from version control, and redact request headers from logs. <br>
Risk: Binding the local proxy beyond localhost could expose the user's Azure OpenAI resource to unintended clients. <br>
Mitigation: Keep the proxy bound to 127.0.0.1 unless intentional network exposure is required and protected. <br>
Risk: The release is Markdown-only and references a proxy script the package does not include. <br>
Mitigation: Inspect any proxy script added or run separately before execution and confirm it matches the documented behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/azure-gateway-cli-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, environment variable examples, and troubleshooting notes.] <br>
**Output Parameters:** [Azure OpenAI endpoint, deployment name, API version, local port, bind address, and API key supplied by the user.] <br>
**Other Properties Related to Output:** [The artifact is a Markdown-only guide; it does not include executable proxy source in this release.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
