## Description: <br>
Route AI agent compute tasks to the cheapest viable backend, supporting local inference with Ollama, cloud GPU execution with Vast.ai, and quantum hardware with Wukong 72Q. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adjusternwachukwu-bot](https://clawhub.ai/user/adjusternwachukwu-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose where an AI compute task should run, check backend availability, and optionally execute workloads through local, cloud GPU, or quantum routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Executing a job may send prompts, payloads, or model inputs to a third-party compute-routing service. <br>
Mitigation: Use route, backend status, health, or stats checks before execute, and do not send secrets, private prompts, proprietary data, credentials, or regulated data unless the provider is trusted and approved for that data. <br>
Risk: Routing work to cloud GPU or quantum backends may create cost, billing, or data-handling exposure beyond local execution. <br>
Mitigation: Review the selected backend and expected cost before execution, and prefer local or recommendation-only routes when the task does not require remote compute. <br>


## Reference(s): <br>
- [Edge Router API](https://edge-router.gpupulse.dev/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/adjusternwachukwu-bot/edge-router) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend route, status, stats, health, or execute API calls for local, cloud GPU, and quantum backends.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
