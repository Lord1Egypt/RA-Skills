## Description: <br>
DanceTempo gives agents concise project context for DanceTempo and DanceTech Protocol work, including llm-full bundle usage, CLAWHUB debugging notes, MPP/x402 routes, OpenAPI discovery, and optional OpenClaw bootstrap reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to orient coding agents in the DanceTempo repository, especially for MPP/x402 payment flows, Tempo network work, OpenAPI discovery, server routing, documentation bundle regeneration, and optional OpenClaw hook setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional OpenClaw hook changes future agent bootstrap context by adding a DanceTempo reminder. <br>
Mitigation: Enable the hook only for workspaces where that reminder is desired, and disable it when the project context is no longer relevant. <br>
Risk: Project memory notes can accidentally expose credentials or private debugging details if copied into agent context. <br>
Mitigation: Keep CLAWHUB.md and related context notes free of secrets and use environment variable names rather than values. <br>
Risk: Agents may act on stale generated documentation after source documentation changes. <br>
Mitigation: Regenerate public/llm-full.txt with npm run build:llm after editing files that feed the bundle. <br>


## Reference(s): <br>
- [DanceTempo ClawHub Listing](https://clawhub.ai/arunnadarasa/dancetempo) <br>
- [Publisher Profile](https://clawhub.ai/user/arunnadarasa) <br>
- [Copilot and Generic Agent Guidance](references/copilot-and-agents.md) <br>
- [DanceTempo Examples](references/examples.md) <br>
- [OpenClaw and DanceTempo](references/openclaw-dancetempo.md) <br>
- [DanceTempo Troubleshooting](references/troubleshooting.md) <br>
- [LLM Bundle Sources](assets/LLM-BUNDLE-SOURCES.md) <br>
- [EVVM Protocol Context](https://www.evvm.info/llms-full.txt) <br>
- [MPPScan Discovery](https://www.mppscan.com/discovery) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces repository orientation, debugging workflow guidance, and optional hook setup instructions for an agent.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
