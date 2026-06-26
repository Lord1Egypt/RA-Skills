## Description: <br>
Agent Work Receipts provides an end-to-end safe coding-agent workflow using BuiltByEcho CLIs for repo preflight, command evidence, final receipts, and CI dry-run planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[builtbyecho](https://clawhub.ai/user/builtbyecho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to orient in a repository, record command evidence, produce human-readable work receipts, and plan CI changes before modifying project automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs BuiltByEcho npm tools and may execute project test, lint, or build commands. <br>
Mitigation: Install and run it only in repositories where those tools and commands are acceptable, and review command output before relying on it. <br>
Risk: Generated briefs, run logs, and trust logs can contain repository details or sensitive command output. <br>
Mitigation: Keep AGENT_BRIEF.md, AGENT_HANDOFF.md, .agent-runs, and .trustlog local by default, and review or redact them before sharing. <br>
Risk: Vaultline upload can persist selected artifacts outside the local workspace. <br>
Mitigation: Set VAULTLINE_API_KEY and run the upload example only when external persistent storage is intentional. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Node.js code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local AGENT_BRIEF.md, AGENT_HANDOFF.md, .agent-runs, and .trustlog artifacts when the referenced commands are run; optional Vaultline upload requires VAULTLINE_API_KEY.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
