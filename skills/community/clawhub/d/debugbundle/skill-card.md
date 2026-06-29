## Description: <br>
Use DebugBundle MCP and CLI workflows to investigate runtime errors/failures, fetch bundles, manage operational debugging surfaces, run verification, and guide fixes when captured operational evidence is relevant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debugbundle](https://clawhub.ai/user/debugbundle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate production or customer-facing incidents, runtime failures, endpoint downtime, DebugBundle bundles, health checks, probes, alerts, and hosted operational workflows. It helps agents fetch relevant operational evidence, run verification, and guide fixes when live debugging context is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use member tokens or existing CLI authentication to access hosted DebugBundle operations. <br>
Mitigation: Provide credentials only when hosted operations are intended, never print tokens or authorization headers, and keep project tokens limited to ingestion-only use. <br>
Risk: The skill directs agents to read and follow project-local DebugBundle instructions after setup. <br>
Mitigation: Install and run it only in trusted repositories and review any project-local `.agents/skills/debugbundle/SKILL.md` before relying on it. <br>
Risk: Management surfaces can change projects, members, alerts, webhooks, GitHub dispatch settings, billing, capture policy, and improvement settings. <br>
Mitigation: Read current state first, explain the intended change, and perform mutations only after the user explicitly asks for them. <br>
Risk: Hosted health checks and probes can target external services or collect additional runtime evidence. <br>
Mitigation: Prefer short TTLs and scoped labels for probes, and avoid private, localhost, metadata-service, credentialed, or state-mutating health-check targets. <br>


## Reference(s): <br>
- [DebugBundle MCP documentation](https://debugbundle.com/docs/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize authorized operational evidence from DebugBundle MCP or CLI workflows; no special post-processing required.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
