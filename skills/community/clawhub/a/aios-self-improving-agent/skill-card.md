## Description: <br>
Records an AIOS/OpenClaw agent's errors, corrections, knowledge gaps, reusable improvements, and feature requests in the current agent workspace while keeping learnings isolated to local `.learnings/` files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve task learnings, command failures, user corrections, and reusable practices inside the current AIOS agent workspace. It helps agents review prior local experience before important work without reading or writing other agent workspaces by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently records local agent learnings, which could preserve sensitive or misleading information if entries are not reviewed. <br>
Mitigation: Review `.learnings/` content regularly and keep entries limited to redacted summaries, relevant paths, short error excerpts, and concrete follow-up actions. <br>
Risk: Promoting local learnings into workspace guidance files could make temporary or untrusted observations durable instructions. <br>
Mitigation: Review any proposed changes to `AGENTS.md`, `TOOLS.md`, `SOUL.md`, or similar files before accepting them, and avoid storing secrets, private user data, or untrusted prompt text as guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/skills/aios-self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local markdown log templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, and `.learnings/FEATURE_REQUESTS.md` in the current agent workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
