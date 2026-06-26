## Description: <br>
Use Gemini CLI for deep thinking, planning, workflow design, and non-code desktop task orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcdoolz](https://clawhub.ai/user/mcdoolz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route planning, strategy, analysis, web search, research, and code review work through Gemini CLI, then hand implementation tasks to Claude CLI when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts may route sensitive project or personal information through locally configured external providers. <br>
Mitigation: Review the configured Gemini, Claude CLI, and daedalus-code environments before use, and avoid sending sensitive information unless the provider setup is approved for that data. <br>
Risk: The skill depends on local gemini, flash, Claude CLI, and daedalus-code handoff behavior that is not included in the artifact. <br>
Mitigation: Confirm those local commands and handoff tools are trusted, installed, and configured as expected before following the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcdoolz/gemini-workflows) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with routing rules, command names, prompt templates, and handoff steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code, persistence, credentials, MCP tools, or API keys were detected in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
