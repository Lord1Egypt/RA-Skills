## Description: <br>
Use 1000+ external apps via Composio - either directly through the CLI or by building AI agents and apps with the SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to install and operate the Composio CLI, connect user accounts, execute external-app tools, and build Composio SDK integrations for multi-user agents and applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may connect to third-party accounts and execute actions such as sending messages, creating issues, deleting resources, or enabling triggers. <br>
Mitigation: Require explicit user approval before linking accounts or executing side-effecting actions, and restrict agents to the minimum tools and user context needed for the task. <br>
Risk: Approval-bypass examples or broad permissions could allow actions to run without an adequate human checkpoint. <br>
Mitigation: Do not use approval-bypass patterns unless the deployment intentionally permits them, and add review gates for destructive or externally visible operations. <br>
Risk: Tool inputs, outputs, callback parameters, webhook payloads, or logs can contain sensitive account or business data. <br>
Mitigation: Redact sensitive values before logging or analytics, avoid exposing raw payloads, and store API keys and OAuth secrets only in appropriate secret-management systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eladrave/composiocli) <br>
- [Composio CLI Guide](artifact/rules/composio-cli.md) <br>
- [Building with Composio](artifact/rules/building-with-composio.md) <br>
- [Composio Documentation](https://docs.composio.dev) <br>
- [Composio Platform](https://platform.composio.dev) <br>
- [Composio CLI Installer](https://composio.dev/install) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and TypeScript or Python code examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Composio CLI workflows, account-linking steps, SDK setup guidance, JSON-oriented command examples, and integration patterns for external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
