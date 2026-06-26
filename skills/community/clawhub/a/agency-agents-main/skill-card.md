## Description: <br>
Agency Agents Main is a role-switching skill pack that lets an agent activate specialized professional personas across engineering, design, business, support, finance, strategy, and other domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keda118228-dev](https://clawhub.ai/user/keda118228-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business users use this skill to switch an assistant into a specialized role for domain-specific guidance, drafting, code work, research, workflow design, and operational planning. It can also serve as a reusable roster of prompt-defined agents for multiple CLI and coding-assistant integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some roles can guide external API use, social-account publishing, scheduling, or account changes. <br>
Mitigation: Require explicit human approval before posts, purchases, account updates, scheduling actions, or other external side effects. <br>
Risk: Some roles and integrations may require OAuth tokens, sensitive credentials, wallet access, or other privileged configuration. <br>
Mitigation: Use least-privilege credentials, keep secrets out of prompt files, and avoid enabling wallet or credential-backed actions unless the execution environment enforces approval gates. <br>
Risk: The artifact includes shell scripts and role prompts that may produce local file edits, shell commands, or generated code. <br>
Mitigation: Review scripts and generated code before execution, run commands in a controlled workspace, and avoid applying broad file changes without a diff review. <br>
Risk: The optional memory integration can persist project context across sessions. <br>
Mitigation: Enable persistent memory only with a trusted MCP server, restrict stored data to non-sensitive context, and review memory contents before reuse across projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keda118228-dev/agency-agents-main) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Security policy](artifact/SECURITY.md) <br>
- [MCP memory integration](artifact/integrations/mcp-memory/README.md) <br>
- [Installation script](artifact/scripts/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code blocks, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the activated role and may include plans, reviews, implementation guidance, commands, configuration examples, or draft deliverables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
