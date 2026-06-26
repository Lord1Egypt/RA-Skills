## Description: <br>
Use when the user wants to analyze local AI coding assistant session data from Claude Code, Codex, and Kimi Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanktechnology](https://clawhub.ai/user/tanktechnology) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to summarize local AI coding assistant sessions, compare tool usage, inspect project activity, and identify patterns or friction across recent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts inspect local AI assistant histories that may contain private project names, file paths, shell commands, and conversation details. <br>
Mitigation: Install and run the skill only when that local-history inspection is intended, and treat terminal output and generated reports as private. <br>
Risk: The optional HTML report embeds sensitive session details and may load a CDN script. <br>
Mitigation: Avoid sharing or publicly hosting generated reports, and use the no-open option when the report should not open automatically in a browser. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanktechnology/ai-session-analysis) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [Skill reference](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Terminal text summaries and optional self-contained HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HTML report embeds local session details and should be treated as private.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
