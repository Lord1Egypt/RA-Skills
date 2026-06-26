## Description: <br>
AI DevOps Toolkit provides observability workflows for local Ollama Herd fleets, including health checks, request tracing, latency analysis, capacity planning, and SQLite-backed analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect local LLM fleet health, investigate failed or slow requests, analyze per-application usage, and plan capacity for Ollama Herd deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational commands could affect local fleet services, models, logs, or project data if run without review. <br>
Mitigation: Review commands before execution, get explicit confirmation before service restarts or model changes, and avoid modifying ~/.fleet-manager contents unless the user requests it. <br>
Risk: Fleet traces, tags, logs, and usage analytics may expose operational or application-level information. <br>
Mitigation: Keep credentials scoped to the intended environment and avoid sharing command output that contains sensitive request, node, or usage details. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/ai-devops-toolkit) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd project repository linked by the skill](https://github.com/geeks-accelerator/ollama-herd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, SQL, and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Ollama Herd router and access to the documented SQLite database and JSONL log paths.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
