## Description:

Beddel helps agents create, validate, run, and debug declarative YAML AI workflows with branching, retries, guardrails, multi-provider LLM calls, and OpenTelemetry tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[botanarede](https://clawhub.ai/user/botanarede)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Beddel to author, validate, run, and troubleshoot YAML-defined AI pipelines and multi-step LLM chains. It is also useful for installing and verifying the Beddel OpenClaw plugin and documenting workflow primitives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflows can install packages or plugins and run local commands or delegated agents.

Mitigation: Install only trusted Beddel packages and plugins, review workflow YAML before execution, and prefer pinned package and plugin versions.

Risk: Workflow inputs, environment variables, prompts, or tool outputs may expose secrets to local tools, delegated agents, or configured LLM providers.

Mitigation: Avoid running untrusted YAML, keep secrets in environment variables, and do not pass secrets into prompts or tool outputs.

Risk: Serving workflows or using shell_exec, agent-exec, $env variables, or plugin installation can expand the runtime attack surface.

Mitigation: Review those workflow features before use and avoid enabling them for untrusted workflows.

## Reference(s):

- [Beddel ClawHub Skill Page](https://clawhub.ai/botanarede/skills/beddel)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)
- [Workflow YAML Format](references/workflow-format.md)
- [Primitives Reference](references/primitives.md)
- [Execution Strategies](references/execution-strategies.md)
- [Variable Resolution](references/variable-resolution.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow YAML, validation guidance, command lines, plugin setup steps, and troubleshooting notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
