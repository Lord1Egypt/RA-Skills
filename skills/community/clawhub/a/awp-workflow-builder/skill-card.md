## Description: <br>
Generate complete Agent Workflow Protocol (AWP) compliant multi-agent workflows from natural language descriptions, including workflow.awp.yaml, agent configs, prompts, schemas, and optional custom tools and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veegee82](https://clawhub.ai/user/veegee82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn a natural language workflow request into an AWP-compliant multi-agent project with manifests, agent definitions, prompts, schemas, and optional runtime adapters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflows can include broad shell, file-write, network, and persistent-memory capabilities. <br>
Mitigation: Use the skill in a dedicated workspace and review the generated plan, YAML, prompts, MCP tools, adapter files, memory settings, and secrets configuration before running anything. <br>
Risk: Generated workflows may send prompts or outputs to third-party LLM or API providers. <br>
Mitigation: Confirm model and provider configuration, API keys, and data handling expectations before executing workflows that call external services. <br>
Risk: Generated MCP tools and adapters may create runnable code with security-sensitive behavior. <br>
Mitigation: Inspect generated tool implementations and adapter configuration, especially shell.execute, infra.run_command, http.request, file.write, broadcast messaging, and persistent memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veegee82/awp-workflow-builder) <br>
- [Publisher profile](https://clawhub.ai/user/veegee82) <br>
- [AWP Specification Summary](references/spec-summary.md) <br>
- [AWP Architecture Overview](references/architecture.md) <br>
- [AWP Validation Rules](references/validation-rules.md) <br>
- [AWP Built-in Tools Reference](references/tools-reference.md) <br>
- [AWP Compliance Levels](references/compliance-levels.md) <br>
- [Standalone adapter](adapters/standalone.md) <br>
- [ClawHub adapter](adapters/clawhub.md) <br>
- [Cloudflare Dynamic Workers adapter](adapters/cloudflare-dynamic-workers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance plus generated project files such as YAML, JSON schemas, Python, TypeScript, prompts, and adapter configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce runnable workflow scaffolds, MCP tool templates, platform adapter files, and follow-up instructions for review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
