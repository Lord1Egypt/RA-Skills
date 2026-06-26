## Description: <br>
Execute declarative YAML AI workflows with branching, retry, multi-provider LLM support, guardrails, and OpenTelemetry tracing via the Beddel Python SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[botanarede](https://clawhub.ai/user/botanarede) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create, validate, run, debug, and serve declarative YAML workflows for multi-step LLM pipelines, automation, guardrails, and observability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Beddel YAML can execute local automation through shell_exec, plugin installation, and delegated-agent steps. <br>
Mitigation: Review each workflow before execution, run with read-only sandboxing where possible, and add allowlists or confirmation gates for shell_exec, plugin-install, and agent-exec steps. <br>
Risk: Workflows can read environment variables through $env references, including API keys. <br>
Mitigation: Run workflows with a minimal environment and provide only the specific credentials needed for the selected LLM provider. <br>
Risk: Untrusted or LLM-generated workflows may request broad local command or agent authority. <br>
Mitigation: Avoid running untrusted workflows directly; validate YAML first and require human approval for commands, external agent delegation, and network-affecting installation steps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/botanarede/beddel) <br>
- [Publisher Profile](https://clawhub.ai/user/botanarede) <br>
- [Workflow YAML Format](artifact/references/workflow-format.md) <br>
- [Primitives Reference](artifact/references/primitives.md) <br>
- [Execution Strategies](artifact/references/execution-strategies.md) <br>
- [Variable Resolution](artifact/references/variable-resolution.md) <br>
- [Bundled Setup Workflow](artifact/examples/setup-beddel.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, Bash, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include workflow files, CLI commands, validation guidance, and OpenClaw plugin setup steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
