## Description: <br>
AI Harness Engineering helps OpenClaw record verified mistakes, hallucinations, defects, feature requests, and lessons into traceable ledgers that support review and self-improvement workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to capture corrected errors, recurring lessons, and feature requests, then query or review those ledgers before future answers. It also supports optional scheduled promotion and summary injection so repeated lessons can inform persistent workspace guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create an always-on local memory that stores conversation-derived content and may write promoted lessons into persistent agent instruction files. <br>
Mitigation: Enable it only when this behavior is desired; review or disable auto-promotion, avoid recording secrets or proprietary details, prune ledgers periodically, and require approval before writing to SOUL.md, AGENTS.md, TOOLS.md, or MEMORY.md. <br>


## Reference(s): <br>
- [AI Harness Engineering on ClawHub](https://clawhub.ai/sqlskills/ai-harness-engineering) <br>
- [sqlskills Publisher Profile](https://clawhub.ai/user/sqlskills) <br>
- [Common Error Patterns](references/error_patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSONL record schemas and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSONL ledgers and workspace guidance files when its scripts are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
