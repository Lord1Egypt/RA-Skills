## Description:

Generate complete Agent Workflow Protocol (AWP) compliant multi-agent workflows from natural language descriptions, including workflow manifests, agent configs, prompts, schemas, and optional tools and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veegee82](https://clawhub.ai/user/veegee82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a natural-language workflow request into a structured AWP project with agent roles, DAG orchestration, output schemas, prompts, platform adapters, and optional MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Cloudflare deployments can expose callable workflow endpoints.

Mitigation: Require authentication and review endpoint access controls before deployment.

Risk: Generated workflows may include privileged tool access such as shell execution, filesystem writes, or broad network access.

Mitigation: Remove shell.execute unless required, enable a real sandbox, and apply filesystem and network allowlists.

Risk: Provider credentials and LLM endpoints can be misconfigured or overexposed.

Mitigation: Restrict LLM endpoints, use provider-specific secrets, and avoid exposing API keys to prompts or generated artifacts.

Risk: Generated memory and logs can retain sensitive workflow data.

Mitigation: Define retention and deletion rules for long-term memory, daily logs, and agent output history.

Risk: Generated dependencies and templates may drift without reproducible installs.

Mitigation: Pin dependencies with a lockfile and review generated code before running or publishing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veegee82/skills/awp-workflow-builder)
- [AWP Specification Summary](references/spec-summary.md)
- [AWP Architecture Overview](references/architecture.md)
- [AWP Validation Rules](references/validation-rules.md)
- [AWP Built-in Tools Reference](references/tools-reference.md)
- [AWP Compliance Levels](references/compliance-levels.md)
- [Standalone Adapter](adapters/standalone.md)
- [Cloudflare Dynamic Workers Adapter](adapters/cloudflare-dynamic-workers.md)
- [ClawHub Adapter](adapters/clawhub.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated YAML, JSON, Python, TypeScript, and shell command snippets or files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces AWP workflow artifacts such as workflow.awp.yaml, agent.awp.yaml, SYSTEM_PROMPT.md, 00_INTRO.md, output schemas, adapters, and optional MCP tool implementations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
