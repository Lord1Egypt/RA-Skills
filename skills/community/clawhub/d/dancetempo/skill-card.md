## Description:

DanceTempo gives agents concise context for the DanceTech Protocol repository, including llm-full.txt, CLAWHUB debugging notes, Tempo MPP/x402 patterns, EVVM links, and OpenAPI discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to onboard agents to DanceTempo repo context, locate debugging history, regenerate the LLM context bundle, and verify Tempo MPP/x402 and OpenAPI routes before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional OpenClaw hook adds a virtual reminder file to each new main agent session.

Mitigation: Enable the hook only when that persistent context reminder is desired, and disable it with the documented OpenClaw command when it is not.

Risk: The skill suggests npm, curl, copy, and hook-enable commands that affect the local repo or agent environment.

Mitigation: Treat commands as manual actions, review them before execution, and run server checks against the intended local port.

Risk: Prompts or debugging notes could accidentally include real environment secret values.

Mitigation: Use environment variable names from .env.example only and avoid putting real .env values into agent prompts.

Risk: The generated llm-full.txt context can drift from edited source documentation.

Mitigation: Regenerate the bundle with npm run build:llm after editing listed source files and verify relevant API routes before relying on the bundle.

## Reference(s):

- [DanceTempo ClawHub Skill](https://clawhub.ai/arunnadarasa/skills/dancetempo)
- [OpenClaw + DanceTempo](references/openclaw-dancetempo.md)
- [DanceTempo Examples](references/examples.md)
- [DanceTempo Troubleshooting](references/troubleshooting.md)
- [Copilot & Generic Agents](references/copilot-and-agents.md)
- [LLM Bundle Sources](assets/LLM-BUNDLE-SOURCES.md)
- [MPPScan Discovery](https://www.mppscan.com/discovery)
- [EVVM LLM Context](https://www.evvm.info/llms-full.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, URLs, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally add an OpenClaw virtual bootstrap reminder file when the hook is enabled.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
