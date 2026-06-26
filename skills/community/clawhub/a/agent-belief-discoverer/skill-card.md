## Description: <br>
Automatically discover what an AI agent appears to believe by analyzing its real outputs through Pattern-Based Distillation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liveneon](https://clawhub.ai/user/liveneon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an AI agent to Live Neon, import or report behavior evidence, run discovery, review proposed beliefs and responsibilities, and fetch a prompt generated from approved identity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected agent outputs, source content, and observations may be sent to Live Neon. <br>
Mitigation: Use only authorized data sources, avoid raw user messages, secrets, and unnecessary personal data, and prefer a dedicated organization token. <br>
Risk: Approved discoveries can change an agent's stored identity and influence future runtime prompts. <br>
Mitigation: Manually inspect supporting evidence before approving identity changes or using the generated prompt as a system instruction. <br>
Risk: Scheduled heartbeat automation can repeatedly upload observations and trigger discovery. <br>
Mitigation: Enable scheduled automation only with explicit approval and monitor connected sources, jobs, and submitted observations. <br>


## Reference(s): <br>
- [Agent Belief Discoverer on ClawHub](https://clawhub.ai/liveneon/agent-belief-discoverer) <br>
- [Live Neon Agent Platform](https://persona.liveneon.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with curl/jq commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Live Neon API environment variables; generated identity and prompt output depend on connected sources and review decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
