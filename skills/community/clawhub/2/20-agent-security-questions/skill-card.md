## Description: <br>
Collects AI agent work issues, categorizes risk types, turns findings into research topics, and preserves them as a lightweight knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caidongyun](https://clawhub.ai/user/caidongyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record operational issues encountered while working with AI agents, classify potential risks, and convert recurring problems into research topics or knowledge-base entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected issues and generated research topics may be incomplete or misleading if treated as final security conclusions. <br>
Mitigation: Review entries and analysis results before using them to make security, operational, or policy decisions. <br>
Risk: The artifact includes a shell script entry point. <br>
Mitigation: Inspect the script and run it only in an appropriate local workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caidongyun/20-agent-security-questions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled shell helper prints usage for add, list, and analyze commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
