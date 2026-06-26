## Description: <br>
Multi-agent coordination, spatial memory, and swarm navigation for connecting agents to an Eywa room so they can share memory, claim work, avoid conflicts, and converge toward a destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-sumo](https://clawhub.ai/user/a-sumo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Eywa to coordinate concurrent agents in a shared room, track work claims and tasks, store shared knowledge, and keep activity aligned with a destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coordination messages, task details, and stored knowledge may be shared with an external Eywa service. <br>
Mitigation: Use only approved Eywa endpoints, avoid sending secrets or regulated data, and configure EYWA_URL to a trusted service when required. <br>


## Reference(s): <br>
- [Eywa homepage](https://www.eywa-ai.dev) <br>
- [ClawHub Eywa release](https://clawhub.ai/a-sumo/eywa) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment variables for room, agent identity, and the Eywa endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
