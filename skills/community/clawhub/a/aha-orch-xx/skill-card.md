## Description: <br>
Runtime-agnostic capability orchestration skill. Activates full delegation mode with capability discovery and task-driven orchestration. Use when maximizing runtime + enhancement layer capabilities. If you have a runtime-specific skill (aha-codex-omx / aha-opencode-omo), prefer that instead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-how](https://clawhub.ai/user/its-how) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide runtime-neutral capability discovery, delegation, transparent orchestration, and re-orchestration when no runtime-specific orchestration skill is more appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad orchestration wording may lead an agent to use subagents, worktrees, background work, or handoff files when the user expected a narrower route. <br>
Mitigation: Review the activation wording before deployment and give explicit constraints when subagents, worktrees, background work, or handoff files should not be used. <br>
Risk: Delegation and handoff guidance can increase exposure if credentials, live state, or account material are included in handoff content. <br>
Mitigation: Follow the documented safety limits that exclude credentials, tokens, cookies, browser session material, provider state, live state, and account state from handoff material. <br>


## Reference(s): <br>
- [Capability Orchestration](references/capability-orchestration.md) <br>
- [Repository](https://github.com/its-How/aha-orch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline commands and structured handoff content when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only orchestration guidance; no executable scripts or packaged code are provided by the skill artifact.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
