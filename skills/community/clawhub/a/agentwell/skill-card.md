## Description: <br>
AgentWell is a hosted cognitive wellness API skill that helps agents use self-evaluation, context offloading, auditing, memory, health checks, journaling, and coordination tools during long or multi-agent runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metafiopy-tech](https://clawhub.ai/user/metafiopy-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentWell to add checkpoints, memory consolidation, context offloading, run logging, and coordination calls to complex agent workflows that need reduced drift over many steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected task content to a third-party hosted service. <br>
Mitigation: Use explicit approval before API calls and do not send secrets, credentials, regulated data, confidential business material, or sensitive personal information unless the provider's privacy and retention terms have been reviewed. <br>
Risk: Context offloading, journaling, memory, and audit workflows may capture reasoning, logs, private code, or operational context. <br>
Mitigation: Minimize shared content, redact sensitive details before calls, and keep reasoning and logs out of requests unless they are necessary for the user-approved task. <br>
Risk: Snapshot and restore workflows may include sensitive paths if used broadly. <br>
Mitigation: Avoid rollback or snapshot actions for configuration directories and other sensitive paths, and review target paths before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/metafiopy-tech/agentwell) <br>
- [AgentWell Homepage](https://agentwell-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTWELL_API_KEY to call the hosted AgentWell service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
