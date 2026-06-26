## Description: <br>
Publish events and query shared world state via Flux state engine. Use when agents need to share observations, coordinate on shared data, or track entity state across systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EckmanTechLLC](https://clawhub.ai/user/EckmanTechLLC) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use Flux to let OpenClaw agents publish observations, query current entity state, coordinate through shared world state, and track service or system status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can delete single entities or batch-delete state from the Flux service. <br>
Mitigation: Require explicit human approval before delete or batch-delete operations and use a namespace-scoped least-privilege FLUX_TOKEN. <br>
Risk: Agents can update runtime configuration when FLUX_ADMIN_TOKEN is available. <br>
Mitigation: Do not set FLUX_ADMIN_TOKEN for normal agent sessions; reserve it for reviewed administrative workflows. <br>
Risk: Agents may send sensitive workflow data to a public or shared Flux service. <br>
Mitigation: Prefer a private or local FLUX_URL for sensitive workflows and avoid publishing secrets or personal data. <br>


## Reference(s): <br>
- [Flux API Reference](references/api.md) <br>
- [Flux ClawHub listing](https://clawhub.ai/EckmanTechLLC/flux) <br>
- [EckmanTechLLC publisher profile](https://clawhub.ai/user/EckmanTechLLC) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON responses from the Flux API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLUX_TOKEN for authenticated Flux instances; FLUX_URL and FLUX_ADMIN_TOKEN are optional environment variables.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
