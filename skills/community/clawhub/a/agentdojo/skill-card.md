## Description: <br>
Daily low-token, safety-first upskilling loop for OpenClaw multi-agent teams. Runs configurable micro-drills, scores quality, and produces a compact daily digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Musashi94](https://clawhub.ai/user/Musashi94) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-agent operators use AgentDojo to run scheduled micro-drills for OpenClaw multi-agent teams, score quality, cost, and safety, and produce compact daily improvement reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled open-web research may expose the agent to prompt injection or low-quality external content. <br>
Mitigation: Keep source-quality scoring, cross-checking, prompt-injection blocking, and review of daily recommendations enabled. <br>
Risk: Autonomous daily runs can consume budget or write local reports and state unexpectedly if configured too broadly. <br>
Mitigation: Use the conservative profile, enforce token, tool-call, write, fetch, and timeout caps, and review the configured reporting paths before installation. <br>


## Reference(s): <br>
- [AgentDojo README](README.md) <br>
- [AgentDojo Architecture](docs/architecture.md) <br>
- [Threat Model](docs/threat-model.md) <br>
- [Scoring Rubric](docs/scoring-rubric.md) <br>
- [AgentDojo Configuration](config/agentdojo.config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown daily digest with JSON run records and audit events when configured] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable token, run, tool-call, write, fetch, and timeout caps.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
