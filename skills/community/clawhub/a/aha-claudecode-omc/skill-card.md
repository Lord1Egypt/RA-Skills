## Description: <br>
Claude Code+OMC optimized capability orchestration skill. Use this when in Claude Code with OMC (oh-my-claudecode) installed. Activates full delegation mode with OMC-specific capability discovery and task-driven orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-how](https://clawhub.ai/user/its-how) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide Claude Code sessions that have OMC installed, so the agent can discover available capability surfaces and select an appropriate orchestration route for each task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct Claude Code to use OMC delegation features, commands, MCPs, worktrees, or orchestration modes available in the local environment. <br>
Mitigation: Install it only when OMC-style delegation is intended, and review OMC plus the available local capability surfaces separately before use. <br>
Risk: Capability availability can vary across sessions, projects, versions, and permission modes. <br>
Mitigation: Run capability discovery for each orchestration pass, skip only unavailable surfaces, and state limitations transparently when discovery is incomplete. <br>


## Reference(s): <br>
- [Capability Orchestration](references/capability-orchestration.md) <br>
- [Aha Orch repository](https://github.com/its-How/aha-orch) <br>
- [OMC repository](https://github.com/Yeachan-Heo/oh-my-claudecode) <br>
- [Claude Code overview](https://docs.anthropic.com/en/docs/claude-code/overview) <br>
- [Claude Code subagents documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides runtime capability discovery, delegation choices, fallback behavior, and transparent re-orchestration.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
