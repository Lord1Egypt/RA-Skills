## Description: <br>
Reference knowledge base for GitHub Copilot CLI features, commands, configuration, plugins, hooks, skills, MCP servers, custom agents, automation, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awalesagar](https://clawhub.ai/user/awalesagar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to answer Copilot CLI questions, set up CLI workflows, configure integrations, and troubleshoot automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad unattended permissions and persistent trust changes can let automated Copilot CLI sessions take actions beyond the intended task. <br>
Mitigation: Prefer scoped --allow-tool and --add-dir patterns, set continuation limits, avoid --yolo or --allow-all with --no-ask-user outside isolated disposable workspaces, and remove trusted_folders entries that are no longer needed. <br>
Risk: Copied examples for remote installers, OAuth or PAT-backed workflows, and raw tool output can expose sensitive data or run untrusted code if used without review. <br>
Mitigation: Review examples before use, do not email raw tool output, verify remote installers before running them, and use least-privilege tokens. <br>


## Reference(s): <br>
- [Copilot CLI documentation](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-copilot-cli) <br>
- [Reference Index](references/index.md) <br>
- [Getting Started](references/getting-started.md) <br>
- [Usage Guide](references/usage.md) <br>
- [Automation, Delegation & Agents](references/automation-and-delegation.md) <br>
- [Customization](references/customization.md) <br>
- [Hooks](references/hooks.md) <br>
- [Integrations](references/integrations.md) <br>
- [Research & Chronicle](references/research.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Patterns and Best Practices](references/patterns-and-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference skill; review generated commands and configuration before use.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
