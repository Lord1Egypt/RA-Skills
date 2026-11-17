## Description: <br>
Helps developers design basic AI agents with prompt engineering, ReAct loop patterns, structured outputs, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and independent builders use this skill to draft system prompts, define agent constraints, design simple ReAct flows, and produce structured output guidance for customer support, data analysis, and other basic agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad local file, search, write, and command-execution authority beyond its core prompt-design purpose. <br>
Mitigation: Install only when that authority is acceptable, and require explicit confirmation before allowing file writes, command execution, API calls, bulk file processing, callback URLs, or API key handling. <br>
Risk: Prompt and ReAct guidance can produce incorrect, unsafe, or overbroad agent behavior if applied without review. <br>
Mitigation: Review generated prompts, constraints, tool permissions, and output schemas before deployment, especially for workflows involving sensitive data or external actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-agent-helper-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with prompt templates, structured examples, JSON snippets, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before use in workflows that write files, run commands, call APIs, process bulk files, or handle secrets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
