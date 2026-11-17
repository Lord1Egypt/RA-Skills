## Description:

Provides agents with Clinical Tempo repository context, troubleshooting guidance, and integration pointers for HealthTech Protocol work across Tempo, MPP/x402, EVVM, OpenAPI, ClawHub, OpenClaw, and related agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to orient coding agents in the Clinical Tempo project, locate authoritative context files, and avoid known troubleshooting traps around MPP/x402, Tempo, EVVM, OpenAPI discovery, hooks, and ClawHub packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional install paths can create persistent agent hook configuration.

Mitigation: Review hook files and enable them only in trusted Clinical Tempo workspaces; disable the hook when persistent reminders are no longer needed.

Risk: External install commands may fetch or execute packages outside the bundled skill.

Mitigation: Pin or verify external packages and commands before running them in production or shared agent environments.

Risk: The scaffold script can create new skill files from user-provided slugs.

Mitigation: Run scaffold scripts only with trusted input and review generated files before publishing or installing them.

## Reference(s):

- [Clinical Tempo ClawHub skill page](https://clawhub.ai/arunnadarasa/skills/clinicaltempo)
- [OpenClaw + Clinical Tempo](references/openclaw-clinical-tempo.md)
- [OpenClaw integration](references/openclaw-integration.md)
- [Troubleshooting](references/troubleshooting.md)
- [Examples](references/examples.md)
- [Copilot and agents](references/copilot-and-agents.md)
- [Hooks setup](references/hooks-setup.md)
- [Agent Skills specification](https://agentskills.io/specification)
- [MPPScan discovery](https://www.mppscan.com/discovery)
- [EVVM LLM context](https://www.evvm.info/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Context-only skill output; optional hooks and scripts may emit reminders or scaffold files when explicitly installed and run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
