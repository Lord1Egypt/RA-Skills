## Description: <br>
Aha Codex Omx helps Codex agents with OMX installed discover, select, combine, and reselect available capability surfaces for task-driven orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[its-how](https://clawhub.ai/user/its-how) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Codex users and developers with OMX installed use this skill to route work across native runtime capabilities, OMX surfaces, skills, MCPs, commands, subagents, and worktrees while keeping orchestration decisions transparent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward broader delegation surfaces such as subagents, worktrees, network access, or external APIs when those surfaces are available. <br>
Mitigation: Review the OMX capabilities available in the environment and keep execution within the runtime permission envelope. <br>
Risk: Partial OMX availability or failed discovery could lead to overclaiming available capabilities. <br>
Mitigation: Run the skill's multi-level pre-check, skip only unavailable surfaces, and state limitations transparently when discovery fails. <br>
Risk: Out-of-session handoff guidance could expose sensitive material if copied without filtering. <br>
Mitigation: Exclude credentials, tokens, cookies, browser session material, provider state, live state, account state, and equivalent secrets from handoff material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/its-how/skills/aha-codex-omx) <br>
- [Repository metadata](https://github.com/its-How/aha-orch) <br>
- [Capability orchestration reference](references/capability-orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No persistent state is maintained by the skill; output depends on the Codex runtime, OMX availability, and configured capability surfaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
