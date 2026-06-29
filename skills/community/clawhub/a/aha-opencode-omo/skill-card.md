## Description: <br>
OpenCode+OMO optimized capability orchestration skill for capability discovery, delegation, and task-driven orchestration in OpenCode with OMO installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-how](https://clawhub.ai/user/its-how) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an OpenCode agent discover available OMO capability surfaces, choose an execution route, delegate work when appropriate, and re-orchestrate when capability gaps appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad delegation, subagent use, or worktree-backed routes can increase side effects, cost, or coordination complexity when over-applied. <br>
Mitigation: Use the skill's permission-envelope checks, confirmation triggers, transparency requirements, and lowest-sufficient-route guidance before delegation. <br>
Risk: Out-of-session handoff material could expose sensitive state if credentials or session data are included. <br>
Mitigation: Follow the documented secret-exclusion rule for credentials, tokens, cookies, browser session material, provider state, live state, and account state. <br>
Risk: Capability discovery can be incomplete or stale when runtime surfaces change across sessions, projects, versions, or permission modes. <br>
Mitigation: Run discovery on each orchestration pass and state uncertainty when discovery fails instead of overclaiming availability. <br>


## Reference(s): <br>
- [Capability Orchestration Reference](references/capability-orchestration.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/its-how/skills/aha-opencode-omo) <br>
- [Repository Metadata URL](https://github.com/its-How/aha-orch) <br>
- [OpenCode](https://github.com/sst/opencode) <br>
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured orchestration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend subagent, worktree, or handoff routes when the active environment and permissions support them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
