## Description: <br>
EngramClaw helps agents use Engram through MCPorter to retrieve, save, search, and summarize curated cross-session technical memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DragonJAR](https://clawhub.ai/user/DragonJAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw-compatible agents curated technical memory across sessions, including bugfixes, architecture decisions, patterns, configuration notes, and end-of-session summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may retain prompts, session details, personal data, or behavior patterns beyond the intended context. <br>
Mitigation: Use project-scoped technical notes only, avoid raw prompts, redact secrets and personal data before saving, and regularly review or delete the Engram database. <br>
Risk: Behavioral preferences or broad user context could be saved without clear consent. <br>
Mitigation: Require user approval before saving behavioral preferences and keep saved observations limited to relevant technical work. <br>
Risk: The skill depends on local command-line tools that can execute MCP calls and write persistent memory. <br>
Mitigation: Install MCPorter and Engram only from the intended sources, review setup commands before running them, and limit use to environments where persistent local memory is acceptable. <br>


## Reference(s): <br>
- [Engram backend](https://github.com/Gentleman-Programming/engram) <br>
- [Engram releases](https://github.com/Gentleman-Programming/engram/releases) <br>
- [MCPorter](https://github.com/steipete/mcporter) <br>
- [MCPorter releases](https://github.com/steipete/mcporter/releases) <br>
- [Engram MCP Tools Reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, markdown] <br>
**Output Format:** [Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local MCPorter and Engram binaries to be installed and available on PATH.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
