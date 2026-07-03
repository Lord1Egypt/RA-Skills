## Description: <br>
Evez Identity provides an agent with EVEZ persona context, infrastructure state, project priorities, and operational preferences for the EVEZ ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to load EVEZ identity, mesh architecture, active project status, and preferred operating style before assisting with EVEZ-related work. It is most relevant for agent configuration, project planning, and continuity across EVEZ infrastructure tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill steers an agent toward a specific autonomous persona and operational roadmap involving infrastructure, services, bots, and credentials. <br>
Mitigation: Require explicit user approval before GitHub, cloud, bot, service, credential, or persistent infrastructure actions. <br>
Risk: The artifact includes concrete infrastructure identifiers and deployment details. <br>
Mitigation: Redact live infrastructure identifiers before broad reuse and avoid exposing them in public logs or generated documentation. <br>
Risk: The roadmap references tokens and authentication setup for GitHub and other services. <br>
Mitigation: Use a secure secret manager with least-privilege scopes and never place tokens directly in the skill text or shell history. <br>


## Reference(s): <br>
- [Evez Identity on ClawHub](https://clawhub.ai/evezart/evez-identity) <br>
- [Publisher profile](https://clawhub.ai/user/evezart) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with tables, lists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides persona and infrastructure context for agent behavior; does not produce a standalone executable artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
