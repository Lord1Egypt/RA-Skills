## Description: <br>
Diagnoses OpenClaw configuration and runtime health for ClawBrain Pro, including output validation, backend model health, knowledge graph status, memory source attribution, degradation notices, and long-conversation truncation checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelfeng](https://clawhub.ai/user/michaelfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw and ClawBrain-backed setups, review likely configuration or runtime issues, and run targeted curl-based health checks against the relevant service endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated curl checks make real external API calls and can expose API keys if copied into shared logs or transcripts. <br>
Mitigation: Review each command before running it, use scoped or low-privilege keys where possible, and avoid sharing logs that contain credentials. <br>
Risk: Graph and memory diagnostics send requests to api.factorhub.cn. <br>
Mitigation: Run those diagnostics only when you are comfortable sending the request to that service and limit checks to the needed troubleshooting scope. <br>


## Reference(s): <br>
- [ClawBrain Doctor on ClawHub](https://clawhub.ai/michaelfeng/clawbrain-pro-doctor) <br>
- [ClawBrain Dashboard](https://clawbrain.dev/dashboard) <br>
- [FactorHub backend health endpoint](https://api.factorhub.cn/v1/health/backends) <br>
- [FactorHub graph stats endpoint](https://api.factorhub.cn/v1/graph/stats) <br>
- [FactorHub models endpoint](https://api.factorhub.cn/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for optional authenticated health, graph, and model endpoint checks.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
